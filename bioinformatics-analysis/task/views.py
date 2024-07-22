# Create your views here.
import mimetypes
import zipfile
import tempfile
import uuid
import os
import json
import csv
from django.db.models import Q, F
import shutil
import subprocess
from datetime import datetime

from django.http import HttpResponse
from django.db import close_old_connections
from rest_framework.views import APIView
from django.http.response import FileResponse
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet

from sample.models import Sample
from project.models import Project
from account.models import Account
from flow.models import Flow
from flow.serializers import FlowSerializer
from project.serializer import ProjectSerializer
from account.serializer import AccountSerializer
from task.models import Task, TaskSample
from task.serializers import TaskSerializer, ListTaskSerializer
from utils.asy import async_func
from utils.hostip import get_host_ip
from utils.message import send_email
from utils.merge_files import merge_files
from utils.paginator import PageNumberPagination
from utils.response import response_body
from utils.kill_process import stop_docker
from django.conf import settings
from flow.models import Flow2Sample
from utils.disk import cal_dir_size
from task.constants import SAMPLE_HEADERS
from account import constants as account_constant
from sample.models import SampleMeta
from patient.models import Patient
from config.models import Config


class TaskView(ModelViewSet):
    queryset = Task.objects.all().select_related('project', "creator", "flow")
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination

    def _enrich_envs(self, envs, sample_objs):
        fields = [field.column for field in Sample._meta.fields]
        for field in fields:
            envs[f"sample_{field}_list".upper()] = ",".join(
                str(getattr(sample, field)) for sample in sample_objs)
        envs["SAMPLE_DIR"] = os.getenv("SAMPLE_DIR")
        envs["BIO_ROOT"] = os.getenv("BIO_ROOT")
        envs["DATA_DIR"] = os.getenv("DATA_DIR")
        envs["DATABASE_DIR"] = os.getenv("DATABASE_DIR")
        envs["TASK_RESULT_DIR"] = os.getenv("TASK_RESULT_DIR")

    def _write_samples_txt(self, task):
        file_path = os.path.join(self._normal_task_dir(task), f"samples.txt")

        with open(file_path, "w") as f:
            f.write("\t".join(SAMPLE_HEADERS))
            f.write("\n")
            for sample in [
                    Sample.objects.get(id=sample_id)
                    for sample_id in sorted(task.samples)
            ]:
                row = self._build_row(task, sample)
                f.write("\t".join([str(item) for item in row]))
                f.write("\n")
        return file_path

    def _build_row(self, task, sample):
        row = []
        sample_meta = SampleMeta.objects.filter(
            id=sample.sample_meta_id).first()
        patient = None
        if sample_meta:
            patient = Patient.objects.filter(id=sample_meta.patient_id).first()
        row.append(sample.project_index)  # 项目编码
        row.append(
            sample_meta.patient_identifier if sample_meta else "")  # 患者识别号
        row.append(sample_meta.identifier if sample_meta else "")  # 样本识别号
        row.append(sample.identifier if sample else "")  # 数据识别号
        row.append(sample.library_number if sample else "")  # 文库编号
        row.append(sample.fastq1_path if sample else "")  # R1文件
        row.append(sample.fastq2_path if sample else "")  # R2文件
        row.append(sample.reagent_box if sample else "")  # 捕获试剂盒
        row.append(sample.library_input if sample else "")  # 建库input
        row.append(sample.index_type if sample else "")  # index类型
        row.append(sample.index_number if sample else "")  # index编号
        row.append(sample.hybrid_input if sample else "")  # 杂交input
        row.append(sample.nucleic_break_type if sample else "")  # 核酸打断方式
        row.append(sample.sample_meta_id if sample else "")  # 样本元信息ID
        row.append(sample.company if sample else "")  # 送检机构
        row.append(sample.risk if sample else "")
        row.append(sample.nucleic_type if sample else "")
        row.append(sample.nucleic_level if sample else "")
        row.append(sample_meta.sample_date if sample_meta else "")
        row.append(sample_meta.test_date if sample_meta else "")
        row.append(sample_meta.sample_componet if sample_meta else "")
        row.append(sample_meta.sample_type if sample_meta else "")
        row.append(sample_meta.panel_proportion if sample_meta else "")
        row.append(sample_meta.is_panel if sample_meta else "")
        row.append(sample_meta.patient_id if sample_meta else "")
        row.append(patient.name if patient else "")
        row.append(patient.gender if patient else "")
        row.append(patient.age if patient else "")
        row.append(patient.birthday if patient else "")
        row.append(patient.id_card if patient else "")
        row.append(patient.location if patient else "")
        row.append(patient.inspection_agency if patient else "")
        row.append(patient.medical_doctor if patient else "")
        row.append(patient.diagnosis if patient else "")
        row.append(patient.tumor_stage if patient else "")
        row.append(patient.disease if patient else "")
        row.append(patient.family_history if patient else "")
        row.append(patient.medication_history if patient else "")
        row.append(patient.treatment_history if patient else "")
        row.append(patient.prognosis_time if patient else "")
        row.append(patient.recurrence_time if patient else "")
        row.append(patient.survival_time if patient else "")

        return row

    def _normal_task_dir(self, task):
        out_dir = os.path.join(settings.TASK_RESULT_DIR, f"{task.creator.id}",
                               f"{task.project.id}",
                               datetime.now().strftime('%Y%m%d'),
                               f"{task.flow.code}", f"{task.id}")
        os.makedirs(out_dir, exist_ok=True, mode=0o733)
        return out_dir

    def has_duplicate(self, req_data):
        flow_id = req_data.get("flow_id")
        if req_data.get("samples"):
            req_data["samples"] = req_data.get("samples").split(",")
        if req_data.get("is_merge") and json.loads(req_data.get("is_merge")):
            task = Task.objects.filter(flow_id=flow_id,
                                       samples=sorted(
                                           req_data.get("samples", [])),
                                       is_merge=True).first()
        else:
            if req_data.get("parameter"):
                req_data["parameter"] = json.loads(req_data.get("parameter"))
            task = Task.objects.filter(
                flow_id=flow_id,
                parameter=req_data.get("parameter", []),
                samples=sorted(req_data.get("samples", [])),
                is_merge=False,
            ).first()
        if task:
            return True, task
        return False, None

    def _upload_task_files(self, request, env):
        out_dir = env["OUT_DIR"]
        for key, file in request.FILES.items():
            filename = os.path.join(out_dir, file.name)
            with open(filename, 'wb+') as fp:
                for chunk in file.chunks():
                    fp.write(chunk)
            env[key] = filename

    def get_flow_memory(self, flow_id):
        flow = Flow.objects.get(id=flow_id)
        return int(getattr(flow, "memory", 1024))

    # 创建归并的任务
    def create_merge_task(self, request):
        req_data = request.POST.copy()
        flow_id = req_data.get("flow_id")
        if req_data.get("parameter"):
            req_data["parameter"] = json.loads(req_data.get("parameter"))
        if req_data.get("samples"):
            req_data["samples"] = req_data.get("samples").split(",")
        req_data["samples"] = sorted(req_data.get("samples", []))
        has_filepath_samples = Flow2Sample.objects.filter(
            flow_id=flow_id).values_list("sample_id", flat=True)
        interation = set([int(item) for item in req_data["samples"]
                          ]) - set(has_filepath_samples)
        if interation:
            interation = [str(item) for item in interation]
            return response_body(code=1,
                                 msg="如下样本id在该流程没有结果: {}".format(
                                     ",".join(interation)))
        # TODO 没有结果的样本不能创建归并
        filepath_list = Flow2Sample.objects.filter(
            flow_id=flow_id,
            sample_id__in=req_data["samples"]).values_list("filepath",
                                                           flat=True)
        task = Task.objects.create(
            **{
                "name": req_data.get('name'),
                "memory": self.get_flow_memory(flow_id),
                "project_id": req_data.get('project_id'),
                "flow_id": req_data.get('flow_id'),
                "samples": req_data["samples"],
                "parameter": req_data.get('parameter', []),
                "creator_id": request.account.id,
                "is_merge": True,
            })
        out_dir = self._normal_task_dir(task)
        env = {
            "OUT_DIR":
            out_dir,
            "TASK_URL":
            f"http://{get_host_ip()}:8000" +
            reverse('task:single', kwargs={'pk': task.id}),
            "IS_MERGE":
            "1",
            "MERGE_SAMPLE_FILES":
            ",".join(filepath_list),
        }
        # env["SAMPLE_DIR"] = os.getenv("SAMPLE_DIR")
        env["BIO_ROOT"] = os.getenv("BIO_ROOT")
        env["DATA_DIR"] = os.getenv("DATA_DIR")
        env["DATABASE_DIR"] = os.getenv("DATABASE_DIR")
        env["TASK_RESULT_DIR"] = os.getenv("TASK_RESULT_DIR")
        task.env = env

        task.save()
        # async_func(merge_files, origin_file_list=filepath_list, dest_dir=out_dir, task_id=task.id)
        serializer = self.get_serializer(task)
        return response_body(data=serializer.data)

    def _check_standard(self, sample_ids, flow_id):
        flow = Flow.objects.get(id=flow_id)
        if not flow.allow_nonstandard_samples:
            for sample_id in sample_ids:
                sample = Sample.objects.filter(id=sample_id).first()
                if sample:
                    if not sample.is_standard:
                        return False
        return True

    def _check_disk(self, request, *args, **kwargs):
        disk_ratio = float(os.getenv("DISK_RATIO", 1))
        disk_config = Config.objects.filter(name="disk").first()
        if (request.account.disk_limit
                and request.account.disk_limit <= request.account.used_disk *
                disk_ratio) or (disk_config.used
                                >= disk_config.value * disk_ratio):
            return True
        return False

    def _check_count(self, request, *args, **kwargs):
        if request.account.task_limit and request.account.task_count >= request.account.task_limit:
            return True
        return False

    def create(self, request, *args, **kwargs):
        if self._check_count(request, *args, **kwargs):
            if request.is_english:
                return response_body(
                    code=1,
                    status_code=400,
                    msg=
                    "Your disk usage has reached the limit. Please delete the space or contact your administrator to increase the disk capacity limit"
                )
            return response_body(code=1,
                                 status_code=400,
                                 msg="您的磁盘使用量已达到限制,请删除空间或联系管理员提高磁盘容量大小限制")
        if self._check_disk(request, *args, **kwargs):
            if request.is_english:
                return response_body(
                    code=1,
                    status_code=400,
                    msg=
                    "Your disk usage has reached the limit. Please delete the space or contact your administrator to increase the disk capacity limit"
                )
            return response_body(code=1,
                                 status_code=400,
                                 msg="您的磁盘使用量已达到限制,请删除空间或联系管理员提高磁盘容量大小限制")
        req_data = request.POST.copy()
        check_duplicate = request.query_params.get("check_duplicate")
        if check_duplicate:
            flag, old_task = self.has_duplicate(req_data)
            if flag:
                return response_body(
                    code=1,
                    msg=
                    f"{old_task.creator.username}已在项目id为{old_task.project.id}创建了任务名称为{old_task.name}的同样的分析任务, 请确认是否继续创建"
                )
            else:
                return response_body(code=200, msg="", data="")
        if req_data.get("is_merge") and json.loads(req_data.get("is_merge")):
            return self.create_merge_task(request)
        # TODO flow 和 样本标准品的校验
        if req_data.get("parameter"):
            req_data["parameter"] = json.loads(req_data.get("parameter"))
        if req_data.get("samples"):
            req_data["samples"] = req_data.get("samples").split(",")
        req_data["samples"] = sorted(req_data.get("samples", []))
        if not self._check_standard(req_data["samples"],
                                    req_data.get('flow_id')):
            return response_body(code=1, msg="该流程只能运行非标准品的样本, 请重新选择")
        req_data["creator_id"] = request.user_id

        env = {
            item["key"]: str(item["value"])
            for item in req_data.get("parameter", [])
        }

        task = Task.objects.create(
            **{
                "name": req_data.get('name'),
                "memory": self.get_flow_memory(req_data.get('flow_id')),
                "project_id": req_data.get('project_id'),
                "flow_id": req_data.get('flow_id'),
                "samples": req_data.get('samples'),
                "parameter": req_data.get('parameter'),
                "creator_id": req_data.get('creator_id'),
                "is_merge": False,
            })
        # env["SAMPLE_DIR"] = os.getenv("SAMPLE_DIR")
        env["BIO_ROOT"] = os.getenv("BIO_ROOT")
        env["DATA_DIR"] = os.getenv("DATA_DIR")
        env["DATABASE_DIR"] = os.getenv("DATABASE_DIR")
        env["TASK_RESULT_DIR"] = os.getenv("TASK_RESULT_DIR")
        out_dir = self._normal_task_dir(task)
        env["OUT_DIR"] = out_dir
        env["TASK_URL"] = f"http://127.0.0.1:8080" + \
                          reverse('task:single', kwargs={'pk': task.id})
        env["SAMPLE_INFO"] = self._write_samples_txt(task)
        env["IS_MERGE"] = "0"
        self._upload_task_files(request, env)
        task.env = env
        task.result_dir = os.path.join(out_dir, "result")
        task.save()
        Account.objects.filter(pk=request.account.pk).update(
            task_count=F("task_count") + 1)
        serializer = self.get_serializer(task)
        for sample_id in task.samples:
            TaskSample.objects.create(sample_id=int(sample_id),
                                      task_id=task.id)
        return response_body(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # 填充igv所需相关信息
        igv_file = os.path.join(instance.env.get('OUT_DIR'), 'result',
                                'IGV_file.txt')
        # os.makedirs(igv_file, exist_ok=True)
        if os.path.exists(igv_file) and os.path.isfile(igv_file):
            with open(igv_file) as f:
                data['igv'] = [line.strip().split('\t') for line in f]
        log_data = instance.log
        log_CN_data = "[]"
        log_EN_data = "[]"
        if not log_data:
            log_CN_data = self._load_CN_log_data(instance)
            log_EN_data = self._load_EN_log_data(instance)
        data["log_CN"] = json.loads(log_CN_data)
        data["log_EN"] = json.loads(log_EN_data)
        return response_body(data=data)

    def _clean_out_dir(self, task):
        out_dir = task.env.get("OUT_DIR")
        if out_dir:
            subprocess.Popen(f"rm -rf {out_dir}", shell=True)
            # async_func(shutil.rmtree, out_dir)

    def _unset_sample_task_id(self, task):
        if task.is_qc:
            Sample.objects.filter(id=task.samples[0]).update(task_id=None)
        if task.is_qc and task.status != 2:
            # 去除qc样本
            try:
                task.project.samples.remove(task.samples[0])
            except Exception as e:
                print(str(e))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self._clean_out_dir(instance)
        self._unset_sample_task_id(instance)
        async_func(
            cal_dir_size,
            dirctory=os.path.join(settings.TASK_RESULT_DIR,
                                  f"{instance.creator.id}"),
            user_id=instance.creator.id,
        )
        try:
            stop_docker(instance.pid)
        except Exception as e:
            print("删除任务时删除容器失败: ", e)
        instance.delete()
        return response_body(data=True)
        # if (request.account.id
        #         == instance.creator.id) or ("admin" in request.role_list):
        #     self._clean_out_dir(instance)
        #     self._unset_sample_task_id(instance)
        #     async_func(
        #         cal_dir_size,
        #         dirctory=os.path.join(settings.TASK_RESULT_DIR,
        #                               f"{instance.creator.id}"),
        #         user_id=instance.creator.id,
        #     )
        #     try:
        #         stop_docker(instance.pid)
        #     except Exception as e:
        #         print("删除任务时删除容器失败: ", e)
        #     instance.delete()
        #     return response_body(data=True)
        # return response_body(code=1, msg="只有管理员和任务创建者可以删除任务", data=False)

    def _enrich_task_list(self, ret_data):
        flow_list = Flow.objects.filter(
            id__in=[item['flow'] for item in ret_data])
        project_list = Project.objects.filter(
            id__in=[item['project'] for item in ret_data])
        account_list = Account.objects.filter(
            id__in=[item['creator'] for item in ret_data])
        sample_list = Sample.objects.filter(id__in=[
            sample_id for item in ret_data for sample_id in item['samples']
        ])

        flow_dict = {flow.id: flow for flow in flow_list}
        project_dict = {project.id: project for project in project_list}
        account_dict = {account.id: account for account in account_list}
        sample_dict = {sample.id: sample for sample in sample_list}

        for item in ret_data:
            item["flow"] = FlowSerializer(flow_dict.get(item['flow'])).data
            item["project"] = ProjectSerializer(
                project_dict.get(item['project'])).data
            item["creator"] = AccountSerializer(
                account_dict.get(item['creator'])).data
            sample_data = []
            for sample_id in item["samples"]:
                sample = sample_dict.get(int(sample_id))
                if sample:
                    obj = {
                        "sample_id": int(sample_id),
                        "sample_data_id": sample.sample_meta_id,
                        "library_number": sample.library_number,
                        "sample_identifier": sample.identifier,
                        "sample_data_identifier": sample.sample_meta.identifier
                    }
                    try:
                        obj["patient_name"] = sample.sample_meta.patient.name
                    except Exception as e:
                        print("task _enrich_task_list error", e)
                        obj["patient_name"] = ""

                    sample_data.append(obj)
            item["sample_data"] = sample_data
        return ret_data

    def list(self, request, *args, **kwargs):
        close_old_connections()

        project_id = request.query_params.get("project_id")
        status = request.query_params.get("status")
        patient = request.query_params.get("patient")
        library_number = request.query_params.get("libraryNumber")
        task_name = request.query_params.get("task_name")
        if account_constant.SUPER in request.role_list:
            tasks = Task.objects.all()
        elif account_constant.ADMIN in request.role_list:
            # project = Project.objects.filter(
            #     projectmembers__account__in=[request.account]).all()
            # tasks = Task.objects.filter(project__in=project)
            # tasks = Task.objects.filter(
            #     Q(creator__user2role__role__code=account_constant.NORMAL) | Q(creator=request.account))
            tasks = Task.objects.filter(
                Q(creator__parent=request.account)
                | Q(creator=request.account))
        else:
            tasks = Task.objects.filter(creator=request.account)
        if project_id:
            tasks = tasks.filter(project_id=project_id)
        if status:
            status_code = {
                value: key
                for key, value in Task.status_choices
            }.get(status)
            tasks = tasks.filter(status=status_code)

        if patient and library_number:
            samples = Sample.objects.filter(
                sample_meta__patient__name=patient,
                library_number=library_number).values_list("id", flat=True)
            tasks = tasks.filter(task_samples__sample_id__in=samples)
        if patient and not library_number:
            samples = Sample.objects.filter(
                sample_meta__patient__name=patient).values_list("id",
                                                                flat=True)
            tasks = tasks.filter(task_samples__sample_id__in=samples)
        if not patient and library_number:
            samples = Sample.objects.filter(
                library_number=library_number).values_list("id", flat=True)
            tasks = tasks.filter(task_samples__sample_id__in=samples)
        if task_name:
            tasks = tasks.filter(name__contains=task_name)
        tasks = tasks.order_by("-create_time")
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = ListTaskSerializer(page, many=True)
            return response_body(
                data={
                    "item_list": self._enrich_task_list(serializer.data),
                    "total_count": tasks.count()
                })

    def _update_sample_bam(self, task):
        if task.is_qc:
            sample = Sample.objects.get(id=task.samples[0])
            out_dir = task.env["OUT_DIR"]
            bam1_path = os.path.join(settings.BAM_PATH, f"{sample.name}",
                                     f"{task.flow.alignment_tool}")
            os.makedirs(bam1_path, exist_ok=True)
            self._copy_files(
                os.path.join(out_dir, "work", sample.name,
                             f"{sample.name}.sorted.bam"), bam1_path)
            self._copy_files(
                os.path.join(out_dir, "work", sample.name,
                             f"{sample.name}.sorted.bam.bai"), bam1_path)
            sample.bam1_path = os.path.join(bam1_path,
                                            f"{sample.name}.sorted.bam")
            sample.save()

    def _copy_files(self, original, dest):
        subprocess.Popen(f"cp -p {original} {dest}", shell=True)

    def _move_result_files(self, task) -> str:
        filename = os.path.basename(task.result_path)
        if task.is_qc:
            # 用户/项目/流程/时间
            dest_dir = os.path.join(settings.MOVE_QC_DIR,
                                    task.creator.username, task.flow.code,
                                    str(task.project.id),
                                    task.create_time.strftime('%Y%m%d'))
        else:
            # 流程/样本/用户/项目/时间/task_id
            dest_dir = os.path.join(settings.MOVE_OTHERS_DIR,
                                    task.creator.username, task.flow.code,
                                    str(task.project.id),
                                    task.create_time.strftime('%Y%m%d'))
        os.makedirs(dest_dir, exist_ok=True)
        dest_filepath = os.path.join(dest_dir, filename)
        self._copy_files(task.result_path, dest_filepath)
        return dest_filepath

    def _update_task_result_path(self, task):
        # dest = self._move_result_files(task)
        # task.result_path = dest
        if task.is_qc:
            self._update_qc_task_result_path(task)
        else:
            self._update_normal_task_result_path(task)

    def _update_qc_task_result_path(self, task):
        sample = Sample.objects.get(id=task.samples[0])
        dest_dir = os.path.join(settings.MOVE_QC_DIR, task.creator.username,
                                str(task.project.id), task.flow.code,
                                task.create_time.strftime('%Y%m%d'),
                                str(task.id), sample.name)
        os.makedirs(dest_dir, exist_ok=True)
        dest_filepath = os.path.join(dest_dir,
                                     os.path.basename(task.result_path))
        self._copy_files(task.result_path, dest_filepath)

        task.result_path = dest_filepath

        Flow2Sample.objects.create(
            **{
                "flow_id": task.flow.id,
                "sample_id": task.samples[0],
                "task_id": task.id,
                "project_id": task.project.id,
                "filepath": dest_filepath
            })

    def _get_sample_by_name(self, name):
        library_type, index_number = name.split("--")
        return Sample.objects.filter(library_type=library_type,
                                     index_number=index_number).first()

    def _update_normal_task_result_path(self, task):
        result_path_list = [
            item.strip() for item in task.result_path.split(",")
        ]
        sample_name_list = [
            os.path.basename(file_path).split(".")[0]
            for file_path in result_path_list
        ]
        dest_filepath_list = []
        for index, sample_name in enumerate(sample_name_list):
            dest_dir = os.path.join(settings.MOVE_OTHERS_DIR,
                                    task.creator.username,
                                    str(task.project.id), task.flow.code,
                                    task.create_time.strftime('%Y%m%d'),
                                    str(task.id), sample_name)
            os.makedirs(dest_dir, exist_ok=True)
            dest_filepath = os.path.join(
                dest_dir, os.path.basename(result_path_list[index]))
            self._copy_files(result_path_list[index], dest_filepath)
            Flow2Sample.objects.create(
                **{
                    "flow_id": task.flow.id,
                    "sample_id": self._get_sample_by_name(sample_name).id,
                    "task_id": task.id,
                    "project_id": task.project.id,
                    "filepath": dest_filepath
                })
            dest_filepath_list.append(dest_filepath)
        task.result_path = ",".join(dest_filepath_list)

    def _update_sample_result_path(self, task):
        dest = task.result_path
        sample = Sample.objects.get(id=task.samples[0])
        sample.result_path = dest
        sample.save()

    def _test_update_task_by_shell(self, task, key, value):
        base = os.path.join(os.path.dirname(settings.BASE_DIR), "task_data")
        os.makedirs(base, exist_ok=True)
        with open(f"{base}/task_{task.id}.txt", "a+") as f:
            f.write(str(key) + " " + str(value) + "\n")

    def _delete_test_update_task_by_shell(self, task):
        base = os.path.join(os.path.dirname(settings.BASE_DIR), "task_data")
        file = f"{base}/task_{task.id}.txt"
        subprocess.Popen(f"rm -rf {file}")

    def _kill_running_task(self, task):
        if task.pid and task.status == 2:
            stop_docker(task.pid)

    def resolve_task_result_path(self, task):
        if task.is_qc:
            self._resolve_qc_task_result_path(task)
        else:
            self._resolve_normal_task_result_path(task)

    def _resolve_qc_task_result_path(self, task):
        # 更新样本bam1_path
        self._update_sample_bam(task=task)
        # 更新样本result_path
        self._update_sample_result_path(task=task)

    def _resolve_normal_task_result_path(self, task):
        async_func(
            send_email,
            subject="任务完成通知",
            to_addr=task.creator.email,
            content=
            f"尊敬的用户，您好！<br/>谢谢使用纳昂达生信分析平台，您在项目{task.project.name}中创建的{task.name}分析已结束，详情见附件，请查收",
            attach={"file": task.result_path.split(",")})

    def _load_CN_log_data(self, instance):
        log_file_CN = os.path.join(instance.env.get("OUT_DIR"), "log_CN.txt")
        data = []
        try:
            with open(log_file_CN, "r") as f:
                for line in f:
                    data.append(json.loads(line.strip()))
        except Exception as e:
            print(f"{instance.id} parse log.txt error: {e}")
        return json.dumps(data, ensure_ascii=False)

    def _load_EN_log_data(self, instance):
        log_file_EN = os.path.join(instance.env.get("OUT_DIR"), "log_EN.txt")
        data = []
        try:
            with open(log_file_EN, "r") as f:
                for line in f:
                    data.append(json.loads(line.strip()))
        except Exception as e:
            print(f"{instance.id} parse log.txt error: {e}")
        return json.dumps(data, ensure_ascii=False)

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        action = request.query_params.get("action", "")
        if instance.status == 5 and ("progress" in request.data
                                     or "status" in request.data
                                     or "result_path" in request.data):
            return response_body(code=1, msg="任务已取消,无法上报信息")
        if action == "cancel" and instance.status in [1, 2]:
            self._kill_running_task(instance)
            instance.status = 5
        elif action == "restart" and instance.status in [4, 5]:
            # TODO logger打印
            self._write_samples_txt(task=instance)
            instance.progress = 0
            instance.status = 1
        for key, value in request.data.items():
            # TODO 换成logger
            self._test_update_task_by_shell(task=instance,
                                            key=key,
                                            value=value)
            if key == "status":
                value = {
                    value: key
                    for key, value in Task.status_choices
                }.get(value)

                async_func(
                    cal_dir_size,
                    dirctory=os.path.join(settings.TASK_RESULT_DIR,
                                          f"{instance.creator.id}"),
                    user_id=instance.creator.id,
                )
            # if key == "priority" and ("admin" not in request.role_list or "super" not in request.role_list):
            #     return response_body(code=1, msg="非管理员用户不能调整优先级")
            setattr(instance, key, value)
            # if key == "result_path" or key == "result_path_CN" or key == "result_path_EN":
            #     # if not instance.is_merge:
            #     #     # 处理result_path
            #     #     self._update_task_result_path(task=instance)
            #     #     # 更新bam, 发送邮件等
            #     #     self.resolve_task_result_path(task=instance)
            #     instance.progress = 100
            #     instance.data = self._load_log_data(instance)
            # TODO 定期删除task_data数据
            # self._delete_test_update_task_by_shell(instance)

        instance.save()
        bs = self.serializer_class(instance, many=False)
        return response_body(data=bs.data)


def download(request, pk):
    if request.is_english:
        file_list = Task.objects.get(id=pk).result_path_EN.split(",")
    else:
        file_list = Task.objects.get(id=pk).result_path_CN.split(",")
    if not file_list:
        return response_body(code=1, msg="要下载的文件不存在,请检查有没有上报结果文件或重新创建任务")

    if len(file_list) == 1:
        filename = os.path.basename(file_list[0])
        with open(file_list[0], "rb") as f:
            data = f.read()
    else:
        filename = "result.zip"
        with tempfile.TemporaryDirectory() as tmpdirname:
            for filepath in file_list:
                if not os.path.exists(filepath):
                    return response_body(code=1,
                                         msg="要下载的文件不存在,请检查有没有上报结果文件或重新创建任务")
                dest = os.path.join(tmpdirname, os.path.basename(filepath))
                os.popen("cp -a {} {}".format(filepath, dest)).readlines()

            os.chdir(tmpdirname)
            dest_filepath = os.path.join(tmpdirname, filename)
            os.popen(f"zip -qr {dest_filepath} .").readlines()

            with open(dest_filepath, "rb") as f:
                data = f.read()

    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename={}'.format(
        filename)
    response['Content-Type'] = 'application/octet-stream'
    return response


def task_summary(request, *args, **kwargs):
    queryset = Task.objects.all()

    if "super" in request.role_list:
        if request.GET.get("start_time__gte"):
            queryset = queryset.filter(
                create_time__gte=request.GET.get("start_time__gte"))
        if request.GET.get("start_time__lte"):
            queryset = queryset.filter(
                create_time__lte=request.GET.get("start_time__lte"))
        return response_body(
            data={
                "pending_task_count": queryset.filter(status=1).count(),
                "running_task_count": queryset.filter(status=2).count(),
                "finished_task_count": queryset.filter(status=3).count(),
                "failured_task_count": queryset.filter(status=4).count(),
                "canceled_task_count": queryset.filter(status=5).count(),
            })
    elif "admin" in request.role_list:
        # queryset = queryset.filter(
        #     Q(creator__user2role__role__code=account_constant.NORMAL) | Q(creator=request.account))
        queryset = queryset.filter(
            Q(creator__parent=request.account) | Q(creator=request.account))
        if request.GET.get("start_time__gte"):
            queryset = queryset.filter(
                create_time__gte=request.GET.get("start_time__gte"))
        if request.GET.get("start_time__lte"):
            queryset = queryset.filter(
                create_time__lte=request.GET.get("start_time__lte"))
        return response_body(
            data={
                "pending_task_count": queryset.filter(status=1).count(),
                "running_task_count": queryset.filter(status=2).count(),
                "finished_task_count": queryset.filter(status=3).count(),
                "failured_task_count": queryset.filter(status=4).count(),
                "canceled_task_count": queryset.filter(status=5).count(),
            })
    else:
        # 普通用户只能查询自己创建的任务
        queryset = queryset.filter(creator_id=request.account)
        # project = Project.objects.filter(
        #     projectmembers__account__in=[request.account]).all()

        if request.GET.get("start_time__gte"):
            queryset = queryset.filter(
                create_time__gte=request.GET.get("start_time__gte"))
        if request.GET.get("start_time__lte"):
            queryset = queryset.filter(
                create_time__lte=request.GET.get("start_time__lte"))
        return response_body(
            data={
                "pending_task_count": queryset.filter(status=1).count(),
                "running_task_count": queryset.filter(status=2).count(),
                "finished_task_count": queryset.filter(status=3).count(),
                "failured_task_count": queryset.filter(status=4).count(),
                "canceled_task_count": queryset.filter(status=5).count(),
            })


def read_file(request, pk):
    task = Task.objects.get(pk=pk)
    file_path = os.path.join(task.result_dir, request.GET['path'])
    ignore_not_existed = request.GET['ignore_not_existed'] or False
    if not os.path.isfile(file_path) or not os.path.exists(file_path):
        return response_body(
            data=None,
            status_code=200,
            code=-1 if not ignore_not_existed else 0,
            msg=f'文件不存在:{file_path}, result_dir:f{task.result_dir}')

    with open(file_path) as f:
        content = f.read()
        return response_body(data=content)


def read_mut_standard_file(request, pk):
    """读取突变 combined.standard-new.csv 文件."""
    task = Task.objects.get(pk=pk)
    name = request.GET['name']

    if name == 'Mut_germline':
        parent_dir = os.path.join(task.result_dir, 'Mut_germline')
    else:
        parent_dir = os.path.join(task.result_dir, 'Mut_somatic')

    files = os.listdir(parent_dir)
    file_path = None
    for item in files:
        if item.endswith('combined.standard-new.csv'):
            file_path = os.path.join(parent_dir, item)
            break
    if file_path is None:
        return response_body(data=None,
                             status_code=200,
                             code=-1,
                             msg=f'文件不存在:{file_path}, result_dir:{parent_dir}')
    with open(file_path) as f:
        content = f.read()
        return response_body(data=content)


class RunQcView(APIView):

    def _qc_task_dir(self, sample):
        return os.path.join(settings.TASK_RESULT_DIR, "qc", f"{sample.id}")

    def post(self, request, *args, **kwargs):
        sample_id = request.data.get("sample_id")
        project = Project.objects.filter(is_builtin=True).first()
        flow = Flow.qc_task()
        sample = Sample.objects.get(id=sample_id)
        qc_data = {
            "name": f"qc_{sample.id}",
            "samples": [sample_id],
            "project_id": project.id,
            "flow_id": flow.id,
            "parameter": [],
            "memory": int(getattr(flow, "memory", 1024)),
            "keep_bam": True,
            "creator_id": request.user_id,
            "is_qc": True
        }

        task = Task.objects.create(**qc_data)
        sample_csv_location = TaskView()._write_samples_txt(task)
        env = {
            "INPUT_DIR":
            os.path.dirname(sample.bam1_path),
            "OUT_DIR":
            TaskView()._normal_task_dir(task),
            "TASK_URL":
            f"http://{get_host_ip()}:8000" +
            reverse('task:single', kwargs={'pk': task.id}),
            "SAMPLE_INFO":
            sample_csv_location,
            "SAMPLE_URL":
            f"http://{get_host_ip()}:8000/sample/samples/{sample.id}",
        }
        task.env = env
        task.save()
        sample.task_id = task.id
        sample.save()
        # add 自带去重
        project.samples.add(sample_id)
        return response_body(data="success", msg="", code=200)


def remove_temp(request, pk):
    instance = Task.objects.get(pk=pk)
    out_dir = instance.env.get("OUT_DIR")
    if out_dir:
        temp_dir = os.path.join(out_dir, "temp")
        subprocess.Popen(f"rm -rf {temp_dir}", shell=True)
        async_func(
            cal_dir_size,
            dirctory=os.path.join(settings.TASK_RESULT_DIR,
                                  f"{instance.creator.id}"),
            user_id=instance.creator.id,
        )
    instance.deleted_tempdir = True
    instance.save()
    return response_body(data="success", msg="", code=200)

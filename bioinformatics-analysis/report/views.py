import os
import json
import threading
import subprocess

from django.db.models import Q
from django.http.request import HttpRequest

from account import constants as account_constant

from task.models import Task
from report.models import Report
from report.core import generate_df, extract_meta_data, extract_data, read_raw_data
from report.constant import FILE_MAPPINGS
from report.serializers import ReportSerializer
from utils.response import response_body
from utils.paginator import PageNumberPaginationWithWrapper
from sample.models import Sample, SampleMeta
from patient.models import Patient
from common.viewsets.viewsets import CustomeViewSets
from model_query.views import ReportSerializer as MReportSerializer


def get_meta_data(request, taskid, name):
    config = FILE_MAPPINGS[name]

    if config.get("type", "csv") == "raw":
        return response_body(data="")

    task = Task.objects.get(id=taskid)
    filename = os.path.join(task.result_dir, config['filepath'])
    columns = json.loads(request.body)
    df = generate_df(filename, sep=config['sep'], header=config['header'])
    return response_body(data=extract_meta_data(df, columns))


def get_raw_data(request, taskid, name):
    config = FILE_MAPPINGS[name]
    task = Task.objects.get(id=taskid)
    filename = os.path.join(task.result_dir, config['filepath'])

    if config.get("type", "csv") == "raw":
        return response_body(data=read_raw_data(filename))

    query = json.loads(request.body)
    df = generate_df(filename, sep=config['sep'], header=config['header'])
    return response_body(data=extract_data(df, query))


def read_file(request):
    """
    读取系统文件
    """
    path = request.GET['path']
    root = os.getenv("BIO_ROOT")
    file = os.path.join(root, path)
    if not os.path.isfile(file) or not os.path.exists(file):
        return response_body(data=None,
                             status_code=200,
                             code=-1,
                             msg=f'文件不存在:{file}, root:{root}')
    with open(file) as f:
        content = f.read()
        return response_body(data=content)


class ReportView(CustomeViewSets):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = PageNumberPaginationWithWrapper

    def create(self, request, *args, **kwargs):
        data = self.create_data(request, *args, **kwargs)
        data['creator_id'] = request.user_id

        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=False)

        if not is_valid:
            return self.deal_with_create_error(serializer)

        script_path = '/data/bioinfo/database_dir/individual_report.py'
        if not os.path.isfile(script_path):
            return response_body(msg='报告脚本不存在')

        report = Report.objects.create(**data)
        report.status = '报告创建中'
        report.save()

        def async_create_report(report):

            # save query to a txt file
            json_filepath = os.path.join(report.task.result_dir, "report",
                                         str(report.id))
            os.makedirs(os.path.dirname(json_filepath), exist_ok=True)
            with open(json_filepath, "w") as fp:
                fp.write(data['query'])

            report_file_path_prefix = os.path.join(report.task.result_dir,
                                                   'report', f'{report.id}')

            # /path/xx.docx不是平台提供给脚本的，如果不增加输入参数，
            # 那这里-o改成报告前缀？ -o /path/xx ，
            # 我脚本生成 /path/xx_CN.docx 和 /path/xx_EN.docx ？

            return_code = subprocess.call([
                'python3', script_path, '-i', json_filepath, '-d',
                os.path.dirname(json_filepath), '-o', report_file_path_prefix
            ])
            print([
                'python3', script_path, '-i', json_filepath, '-d',
                os.path.dirname(json_filepath), '-o', report_file_path_prefix
            ])
            cn_file_path = f'{os.path.abspath(report_file_path_prefix)}_CN.docx'
            en_file_path = f'{os.path.abspath(report_file_path_prefix)}_EN.docx'
            if not os.path.isfile(cn_file_path) or not os.path.isfile(
                    en_file_path):
                report.status = '创建失败'
                report.save()
                return response_body(msg="脚本执行异常")

            # report.report_path = report_file_path
            report.report_path_cn = cn_file_path
            report.report_path_en = en_file_path
            report.status = '创建成功'
            report.save()

        threading.Thread(target=async_create_report,
                         args=(report, ),
                         daemon=True).start()
        return response_body(data=serializer.data, msg="success")

    def post_list(self, data, request, *args, **kwargs):
        return data

    def list(self, request, *args, **kwargs):
        search = request.GET.get('search', None)
        patient_identifier = request.GET.get('patient_identifier', None)
        sample_meta_identifier = request.GET.get('sample_meta_identifier',
                                                 None)
        sample_identifier = request.GET.get('sample_identifier', None)

        filtered = False
        samples = Sample.objects
        if sample_identifier:
            filtered = True
            samples = samples.filter(identifier=sample_identifier)
        if sample_meta_identifier:
            filtered = True
            samples = samples.filter(
                sample_meta__identifier=sample_meta_identifier)
        if patient_identifier:
            filtered = True
            samples = samples.filter(
                sample_meta__patient__identifier=patient_identifier)
        if filtered:
            sample_ids = [str(item.id) for item in samples.all()]
            query = ''
            task_ids = []
            if sample_ids:
                query = f'select id from task where samples ?| ARRAY{sample_ids}'
                if search:
                    query = f'{query} and name ilike \'%%{search}%%\''
                for item in Task.objects.raw(query):
                    task_ids.append(item.id)

            queryset = Report.objects.filter(task__id__in=task_ids)
        else:
            if search:
                queryset = Report.objects.filter(task__name__icontains=search)
            else:
                queryset = Report.objects.all()

        if account_constant.NORMAL in request.role_list:
            queryset = queryset.filter(creator=request.account)
        elif account_constant.ADMIN in request.role_list:
            queryset = queryset.filter(
                Q(creator__user2role__role__code=account_constant.NORMAL)
                | Q(creator=request.account))
        queryset = queryset.order_by('-id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MReportSerializer(page, many=True)
            data = self.post_list(serializer.data, request, *args, **kwargs)
            return self.get_paginated_response(data)

        serializer = MReportSerializer(queryset, many=True)
        data = self.post_list(serializer.data, request, *args, **kwargs)
        return response_body(data=data, msg="success")


def pathogen_read(request):
    task_id=request.GET.get('task_id') # 任务 id
    task = Task.objects.get(id=task_id)
    project = task.project

    # # 项目下的样本 id 列表
    # project_sample_ids = [sample.id for sample in project_samples]

    project_tasks = Task.objects.filter(project=project).all()
    # 项目下所有任务的结果目录
    project_tasks_result = []

    for item in project_tasks:
        task_samples = [
            {
                'project_index': sample.project_index,
                'library_number': sample.library_number,
                'reagent_box': sample.reagent_box,
                'nucleic_break_type': sample.nucleic_break_type,
                'library_input': sample.library_input,
                'index_type': sample.index_type,
                'index_number': sample.index_number,
                'hybrid_input': sample.hybrid_input,
                'risk': sample.risk,
                'nucleic_level': sample.nucleic_level,
                # 'sample_meta':sample.sample_meta,
                'sample_identifier': sample.sample_identifier,
                'identifier': sample.identifier,
                'company': sample.company,
                'nucleic_type': sample.nucleic_type,
                'fastq1_path': sample.fastq1_path,
                'fastq2_path': sample.fastq2_path,
                # 'user':sample.user,
                #'create_time':sample.create_time,
                #'modify_time':sample.modify_time,
            } for sample in Sample.objects.filter(id__in=item.samples).all()
        ]
        task = {
            'id': item.id,
            'name': item.name,
            # 'project':item.project,
            'status': item.status,
            'progress': item.progress,
            # 'creator':item.creator,
            'pid': item.pid,
            'is_merge': item.is_merge,
            # 'flow':item.flow,
            'result_path': item.result_path,
            'result_path_CN': item.result_path_CN,
            'result_path_EN': item.result_path_EN,
            'result_dir': item.result_dir,
            'keep_bam': item.keep_bam,
            'has_cleaned': item.has_cleaned,
            'is_qc': item.is_qc,
            'priority': item.priority,
            'memory': item.memory,
            'log': item.log,
            'error_message': item.error_message,
            'error_message_EN': item.error_message_EN,
            'error_message_CN': item.error_message_CN,
            # 'create_time':item.create_time,
            # 'update_time':item.update_time,
            # 'deleted_tempdir':item.deleted_tempdir,
            'env': item.env,
            'samples': task_samples,
            'parameter': item.parameter,
        }
        project_tasks_result.append(task)
    project_tasks_result.sort(key=lambda item: item['id'])

    return response_body(data=project_tasks_result)

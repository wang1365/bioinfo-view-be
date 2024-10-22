import traceback
import uuid
import tempfile
import time
import os
from typing import Tuple

from common.exceptions import ServiceException
from task.models import Task
from task.serializers import TaskSerializer
from utils.response import response_body
from collections import defaultdict

from django.db.models import Q

from account import constants as account_constant

from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.http import HttpResponse, QueryDict

from patient.models import Patient
from sample.models import Sample, SampleMeta
from sample.core import ExcelHandler, ValueProcess, export_to_csv, export_to_csv_sample_meta
from sample.serializers import SampleMetaSerializer, SampleSerializer, SampleMeta
from sample.filters import (SampleFilters, SampleProjectFilters,
                            SampleUserFilter, SampleKeywordFilters)
from utils.paginator import PageNumberPaginationWithWrapper

from common.viewsets.viewsets import CustomeViewSets

from sample.constants import SAMPLE_META_MODEL_ATTRS, SAMPLE_MODEL_ATTRS, FIELDS_OPERATORS, SearchType
from logging import getLogger

logger = getLogger(__name__)

class SampleView(CustomeViewSets):
    queryset = Sample.objects.prefetch_related('sample_meta').all()
    serializer_class = SampleSerializer
    pagination_class = PageNumberPaginationWithWrapper

    filter_backends = [
        SampleFilters, SampleProjectFilters, SampleUserFilter,
        SampleKeywordFilters
    ]

    def create(self, request, *args, **kwargs):
        data = self.create_data(request, *args, **kwargs)
        data['identifier'] = str(uuid.uuid4())
        data['user'] = request.account.id

        if data['fastq_merge_required']:
            ok, resp = self.merge_fastq(data)
            if not ok:
                return resp

        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=False)

        if not is_valid:
            return self.deal_with_create_error(serializer)

        self.perform_create(serializer)
        obj = serializer.instance
        obj.identifier = f'D{obj.id:08}'
        obj.save()

        return response_body(data=serializer.data, msg="success")

    @staticmethod
    def merge_fastq(data) -> Tuple[bool, object]:
        fp1 = data['fastq1_path_list']
        fp2 = data['fastq2_path_list']
        # 样本数据文件存放的路径
        base_dir = os.getenv("DATA_DIR")
        # fp1和fp2都是以逗号分隔的文件路径，是只包含一个文件文件的.gz格式的压缩文件
        # 需要将这两个文件列表各自合并为一个文件，并且保留原始文件，文件命名以uuid+日期时间戳
        # 例如：uuid_2021-08-01-12-00-00.gz
        # 合并后的文件路径保存到fastq1_path和fastq2_path中
        def merge(fp, out_fp):
            if os.name != 'nt':
                # linux下使用cat命令合并文件
                src_files = ' '.join(fp.split(','))
                os.system(f'cd {base_dir} && cat {src_files} > {out_fp}')
            else:
                # windows下不支持cat命令，使用copy /b命令合并文件
                src_files = '+'.join(fp.split(','))
                os.system(f'cd {base_dir} && copy /b {src_files} {out_fp}')

        out_fp_pattern = f'{uuid.uuid4().hex[:8]}_{time.strftime("%Y%m%d%H%M%S")}_%s.gz'
        out_fp1 = out_fp_pattern % 'R1'
        out_fp2 = out_fp_pattern % 'R2'

        try:
            merge(fp1, os.path.join(base_dir, out_fp1))
            merge(fp2, os.path.join(base_dir, out_fp2))
        except ServiceException as e:
            return False, response_body(status_code=e.status_code, msg=e.message)
        except Exception as e:
            traceback.print_exc()
            return False, response_body(status_code=500, msg=str(e))
        data['fastq1_path'] = out_fp1
        data['fastq2_path'] = out_fp2

        logger.info(f'合并样本数据文件：{fp1} -> {out_fp1}, {fp2} -> {out_fp2}')
        return True, ''


    def post_retrieve(self, data, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        # 添加样本数据关联的任务列表
        tasks = list(Task.objects.filter(samples__contains=[pk]))
        task_data = TaskSerializer(instance=tasks, many=True).data
        data.update({'tasks': task_data})

    def _get_related_tasks(self, sample_ids):
        # 添加样本数据关联的任务列表
        tasks = list(Task.objects.filter(samples__has_any_keys=sample_ids))
        # TODO 任务还需要进行状态过滤

        result = defaultdict(list)
        for task in tasks:
            for id in task.samples:
                if int(id) in sample_ids:
                    out_dir = task.env.get('OUT_DIR') or ''
                    exist_igv = os.path.exists(
                        os.path.join(out_dir, 'result', 'IGV_file.txt'))
                    result[id].append({
                        'id': task.id,
                        'name': task.name,
                        'flow_name': task.flow.name,
                        'flow_id': task.flow.id,
                        'status': task.status,
                        'result_dir': task.result_dir,
                        'out_dir': task.env.get('OUT_DIR'),
                        'exist_igv': exist_igv
                    })
        return result

    def post_list(self, data, request, *args, **kwargs):
        ret = data
        sample_ids = [t['id'] for t in data]
        # 查询样本数据关联的任务列表
        task_map = self._get_related_tasks(sample_ids)
        for sample in data:
            sample['tasks'] = task_map.get(str(sample['id'])) or []
        return ret

    def query(self, request, *args, **kwargs):
        ret = self.list(request, *args, **kwargs)
        return ret

    def list_fields(self, request, *args, **kwargs):
        data = {}

        for field in SAMPLE_MODEL_ATTRS:
            record = {}
            key = field['key']

            if field['search_type'] == SearchType.choices:
                record['choices'] = [
                    f for f in self.queryset.order_by(
                        key).distinct().values_list(key, flat=True) if f
                ]
            record['operators'] = FIELDS_OPERATORS.get(
                (field['value_type'], field['search_type']), ['ne', 'eq'])
            data[key] = record

        return response_body(data=data)

    def export(self, request):
        path = export_to_csv(
            SampleUserFilter().filter_queryset(request, self.queryset, None),
            request.is_english)

        with open(path, "rb") as f:
            data = f.read()

        filename = '{}-{}.csv'.format(request.account.username,
                                      int(time.time() * 100))
        response = HttpResponse(data)
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            filename)
        response['Content-Type'] = 'application/octet-stream'
        return response


class SampleMetaView(CustomeViewSets):
    queryset = SampleMeta.objects.prefetch_related('patient').all()
    serializer_class = SampleMetaSerializer
    pagination_class = PageNumberPaginationWithWrapper

    filter_backends = [SampleFilters, SampleProjectFilters, SampleUserFilter]

    def create(self, request, *args, **kwargs):
        data = self.create_data(request, *args, **kwargs)
        data['identifier'] = str(uuid.uuid4())
        data['user'] = request.account.id

        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=False)

        if not is_valid:
            return self.deal_with_create_error(serializer)

        self.perform_create(serializer)
        obj = serializer.instance
        obj.identifier = f'S{obj.id:08}'
        obj.save()

        return response_body(data=serializer.data, msg="success")

    def query(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list_fields(self, request, *args, **kwargs):
        data = {}

        for field in SAMPLE_MODEL_ATTRS:
            record = {}
            key = field['key']

            if field['search_type'] == SearchType.choices:
                record['choices'] = [
                    f for f in self.queryset.order_by(
                        key).distinct().values_list(key, flat=True) if f
                ]
            record['operators'] = FIELDS_OPERATORS.get(
                (field['value_type'], field['search_type']), ['ne', 'eq'])
            data[key] = record

        return response_body(data=data)

    def export(self, request):
        path = export_to_csv_sample_meta(
            SampleUserFilter().filter_queryset(request, self.queryset, None),
            request.is_english)

        with open(path, "rb") as f:
            data = f.read()

        filename = '{}-{}.csv'.format(request.account.username,
                                      int(time.time() * 100))
        response = HttpResponse(data)
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            filename)
        response['Content-Type'] = 'application/octet-stream'
        return response


class SampleUploadView(CustomeViewSets):
    parser_classes = (MultiPartParser, )

    def upload(self, request, suffix=".xlsx"):
        info = {
            "attrs": SAMPLE_MODEL_ATTRS,
            "serializer": SampleSerializer,
            "identifiers": self._get_sample_meta_identifiers(request),
            "key": "sample_identifier",
            "update_id": self._update_sample_meta_id,
            "prefix": "D",
        }
        return self._upload(request, info, suffix)

    def upload_meta(self, request, suffix=".xlsx"):
        info = {
            "attrs": SAMPLE_META_MODEL_ATTRS,
            "serializer": SampleMetaSerializer,
            "identifiers": self._get_patient_identifiers(request),
            "key": "patient_identifier",
            "update_id": self._update_patient_id,
            "prefix": "S",
        }
        return self._upload(request, info, suffix)

    def _get_sample_meta_identifiers(self, request):
        queryset = SampleMeta.objects.all()
        if account_constant.NORMAL in request.role_list:
            queryset = queryset.filter(user=request.account)
        elif account_constant.ADMIN in request.role_list:
            queryset = queryset.filter(
                Q(user__user2role__role__code=account_constant.NORMAL)
                | Q(user=request.account))
        return queryset.values_list("identifier", flat=True)

    def _get_patient_identifiers(self, request):
        queryset = Patient.objects.all()
        if account_constant.NORMAL in request.role_list:
            queryset = queryset.filter(creator=request.account)
        elif account_constant.ADMIN in request.role_list:
            queryset = queryset.filter(
                Q(creator__user2role__role__code=account_constant.NORMAL)
                | Q(creator=request.account))
        return queryset.values_list("identifier", flat=True)

    def _update_sample_meta_id(self, obj, identifier):
        if identifier[1:].isdigit():
            obj.sample_meta_id = int(identifier[1:])
        else:
            sample_meta = SampleMeta.objects.filter(
                identifier=identifier).first()
            obj.sample_meta_id = sample_meta.id

    def _update_patient_id(self, obj, identifier):
        if identifier[1:].isdigit():
            obj.patient_id = int(identifier[1:])
        else:
            patient = Patient.objects.filter(identifier=identifier).first()
            obj.patient_id = patient.id

    def _upload(self, request, info, suffix='.xlsx'):
        up_file = request.FILES['file']

        _, filename = tempfile.mkstemp(suffix=suffix)

        with open(filename, 'wb+') as fp:
            for chunk in up_file.chunks():
                fp.write(chunk)

        excel_handler = ExcelHandler(filename, info['attrs'],
                                     request.is_english)
        records = excel_handler.read()

        unsuccessful_records = []
        value_process = ValueProcess(user_id=request.account.id)

        for record in records:
            data = value_process.process(record)
            if data[info['key']].strip() not in info['identifiers']:
                unsuccessful_records.append(record)
                continue
            data['identifier'] = str(uuid.uuid4())
            data['user'] = request.account.id

            sample_serializer = info['serializer'](data=data)
            if sample_serializer.is_valid():
                sample_serializer.save()
                obj = sample_serializer.instance
                obj.identifier = info['prefix'] + f'{obj.id:08}'
                info['update_id'](obj, data[info['key']].strip())
                obj.save()
            else:
                print(sample_serializer.errors)
                unsuccessful_records.append(record)

        is_all_success = len(unsuccessful_records) == 0

        return response_body(
            data=unsuccessful_records,
            msg="success" if is_all_success else "part success",
        )


def download(request, pk):
    file = Sample.objects.get(id=pk).result_path
    if not file:
        return response_body(code=1, msg="要下载的文件不存在,请检查任务完成后有没有上报结果文件")
    return download_by_filename(file)


def download_by_choices(request, filenames):
    filename = filenames[request.is_english]
    return download_by_filename(request, filename)


def download_by_filename(request, filename):
    if not filename:
        return response_body(code=1, msg="要下载的文件不存在")
    with open(filename, "rb") as f:
        data = f.read()

    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename={}'.format(
        os.path.basename(filename))
    response['Content-Type'] = 'application/octet-stream'
    return response

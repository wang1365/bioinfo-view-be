import tempfile
import time
import os

from utils.response import response_body

from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.http import HttpResponse

from sample.models import Sample, SampleMeta
from sample.core import ExcelHandler, ValueProcess, export_to_csv
from sample.serializers import SampleMetaSerializer, SampleSerializer, SampleMeta
from sample.filters import (SampleFilters, SampleProjectFilters,
                            SampleUserFilter)
from utils.paginator import PageNumberPaginationWithWrapper

from common.viewsets.viewsets import CustomeViewSets

from sample.constants import SAMPLE_META_MODEL_ATTRS, SAMPLE_MODEL_ATTRS, FIELDS_OPERATORS, SearchType


class SampleView(CustomeViewSets):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    pagination_class = PageNumberPaginationWithWrapper

    filter_backends = [SampleFilters, SampleProjectFilters, SampleUserFilter]

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
        path = export_to_csv(self.queryset.all())

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
    queryset = SampleMeta.objects.all()
    serializer_class = SampleSerializer
    pagination_class = PageNumberPaginationWithWrapper

    filter_backends = [SampleFilters, SampleProjectFilters, SampleUserFilter]

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
        path = export_to_csv(self.queryset.all())

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

    def upload(self, request, suffix=".xlxs"):
        info = {
            "attrs": SAMPLE_MODEL_ATTRS,
            "serializer": SampleSerializer
        }
        return self._upload(request, info, suffix)

    def upload_meta(self, request, suffix=".xlxs"):
        info = {
            "attrs": SAMPLE_META_MODEL_ATTRS,
            "serializer": SampleMetaSerializer
        }
        return self._upload(request, info, suffix)

    def _upload(self, request, info, suffix='.xlxs'):
        up_file = request.FILES['file']

        _, filename = tempfile.mkstemp(suffix=suffix)

        with open(filename, 'wb+') as fp:
            for chunk in up_file.chunks():
                fp.write(chunk)

        excel_handler = ExcelHandler(filename, info['attrs'])
        records = excel_handler.read()

        unsuccessful_records = []
        value_process = ValueProcess(user_id=request.account.id)

        for record in records:
            sample_serializer = info['serializer'](
                data=value_process.process(record))
            if sample_serializer.is_valid():
                sample_serializer.save()
            else:
                print(sample_serializer.errors)
                unsuccessful_records.append(record)

        return response_body(data=unsuccessful_records, msg="success")


def download(request, pk):
    file = Sample.objects.get(id=pk).result_path
    if not file:
        return response_body(code=1, msg="要下载的文件不存在,请检查任务完成后有没有上报结果文件")
    return download_by_filename(file)


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

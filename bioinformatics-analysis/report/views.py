import os
import json

import subprocess

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

        report = Report.objects.create(**data)
        report.save()

        # save query to a txt file
        filepath = os.path.join(report.task.result_dir, "report",
                                str(report.id))
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as fp:
            fp.write(data['query'])

        # execute script with input parameter

        # script_path = os.path.join(os.getenv("BIO_ROOT"), report.script)
        # returncode = subprocess.call(["python3", script_path, filepath])
        # if returncode != 0:
        #     return response_body(msg="execute command error")

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
        samples = Sample.objects()
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
            sample_ids = [item.id for item in samples.all()]
            query = f'select id from task where samples ?| %s'
            args = [sample_ids]
            if search:
                query = f'{query} and name ilike %{search}%'
            task_ids = []
            for item in Task.objects.raw(query, args):
                task_ids.append(item.id)

            queryset = Report.objects.filter(task__id__in=task_ids).all()
        else:
            if search:
                queryset = Report.objects.filter(
                    task__name__icontains=search).all()
            else:
                queryset = Report.objects.all()

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MReportSerializer(page, many=True)
            data = self.post_list(serializer.data, request, *args, **kwargs)
            return self.get_paginated_response(data)

        serializer = MReportSerializer(queryset, many=True)
        data = self.post_list(serializer.data, request, *args, **kwargs)
        return response_body(data=data, msg="success")

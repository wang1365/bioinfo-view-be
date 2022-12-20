"""单个模型使用 post 传递 Q 表达式进行过滤."""
import json

from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from sample.models import Sample, SampleMeta
from patient.models import Patient
from project.models import Project
from task.models import Task
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from utils.query_filter import build_q
from report.models import Report

MODEL_MAP = {
    'sample': Sample,
    'sample_meta': SampleMeta,
    'project': Project,
    'patient': Patient,
    'task': Task,
    'report': Report
}


class SampleMetaSerializer(ModelSerializer):

    class Meta:
        model = SampleMeta
        fields = '__all__'
        depth = 1


class PatientSerializer(ModelSerializer):
    samplemeta_set = SampleMetaSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        depth = 1


class SampleSerializer(ModelSerializer):
    sample_meta = SampleMetaSerializer(read_only=True)

    class Meta:
        model = Sample
        fields = '__all__'
        depth = 1


class TaskSerializer(ModelSerializer):
    sample_set = SampleSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'


SERIALIZER_MAP = {
    # 'sample': SampleSerializer,
    'patient': PatientSerializer,
    'sample': SampleSerializer,
    'report': ReportSerializer
}


def post_query(request: HttpRequest, model_name: str):
    if request.body:
        q_st = json.loads(request.body)
    else:
        return JsonResponse({'code': 1, 'msg': '请求体不可空'})
    model = MODEL_MAP.get(model_name, None)
    if not model:
        return JsonResponse({'code': 1, 'msg': f'只支持{MODEL_MAP.keys()}'})
    q = build_q(q_st)
    query_set = model.objects.filter(q)
    page_size = request.GET.get('size', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(query_set, page_size)
    objs = paginator.page(page)
    serializer = SERIALIZER_MAP.get(model_name, None)
    if not serializer:
        serializer = type(
            'ObjSerializer', (ModelSerializer, ), {
                'Meta':
                type('Meta', (), {
                    'model': model,
                    'fields': '__all__',
                    'depth': 1
                })
            })
        SERIALIZER_MAP[model_name] = serializer
    sobj = serializer(objs, many=True)
    # import ipdb
    # ipdb.set_trace()
    return JsonResponse({
        'code': 0,
        'data': {
            'count': paginator.count,
            'results': sobj.data
        },
        'msg': 'OK'
    })

from django.shortcuts import render

# Create your views here.
from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend

from config.filters import ConfigFilterSet, ResourceFilterSet
from rest_framework.decorators import action

from common.viewsets.viewsets import CustomeViewSets

from config.serializers import ConfigSerializer, ResourceSerializer
from config.models import Config, Resource
from task.models import Task
from utils.paginator import PageNumberPaginationWithWrapper
from utils.disk import dir_size
from utils.response import response_body


class ConfigView(CustomeViewSets):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    pagination_class = PageNumberPaginationWithWrapper
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ConfigFilterSet


class ResourceView(CustomeViewSets):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    pagination_class = PageNumberPaginationWithWrapper
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ResourceFilterSet

    @action(methods=["GET"], detail=False)
    def week(self, request, *args, **kwargs):
        now = datetime.now()
        week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0)
        tasks = Task.objects.filter(create_time__gte=week_start, create_time__lte=now)
        day_used_disk = 0
        for task in tasks:
            day_used_disk += dir_size(task.env.get("OUT_DIR"))
        return response_body(data=day_used_disk)





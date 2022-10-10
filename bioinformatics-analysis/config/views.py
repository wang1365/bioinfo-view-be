from django.shortcuts import render

# Create your views here.
import json

from django_filters.rest_framework import DjangoFilterBackend

from config.filters import ConfigFilterSet
from utils.response import response_body

from common.viewsets.viewsets import CustomeViewSets

from config.serializers import ConfigSerializer
from config.models import Config
from utils.paginator import PageNumberPaginationWithWrapper


class ConfigView(CustomeViewSets):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    pagination_class = PageNumberPaginationWithWrapper
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ConfigFilterSet



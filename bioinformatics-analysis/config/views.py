from django.shortcuts import render

# Create your views here.
import json

from django_filters.rest_framework import DjangoFilterBackend

from config.filters import ConfigFilterSet, ResourceFilterSet
from rest_framework.viewsets import ModelViewSet

from common.viewsets.viewsets import CustomeViewSets

from config.serializers import ConfigSerializer, ResourceSerializer
from config.models import Config, Resource
from utils.paginator import PageNumberPaginationWithWrapper


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



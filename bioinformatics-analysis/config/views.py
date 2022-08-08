from django.shortcuts import render

# Create your views here.
import json
from utils.response import response_body

from common.viewsets.viewsets import CustomeViewSets

from config.serializers import ConfigSerializer
from config.models import Config
from utils.paginator import PageNumberPaginationWithWrapper


class ConfigView(CustomeViewSets):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    pagination_class = PageNumberPaginationWithWrapper



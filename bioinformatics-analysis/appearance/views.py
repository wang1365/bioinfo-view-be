from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from appearance import models
from appearance.serializer import SiteLayOutSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from utils.response import response_body
# Create your views here.

class SiteLayoutlViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    """视图集"""
    queryset = models.SiteLayOut.objects.all()
    serializer_class = SiteLayOutSerializer

    def create(self, request, *args, **kwargs):
        serializer = SiteLayOutSerializer(data=request.data)
        if not serializer.is_valid():
            return response_body(status_code=status.HTTP_400_BAD_REQUEST, msg=serializer.errors)
        with transaction.atomic():
            models.SiteLayOut.objects.all().delete()
            models.SiteLayOut.objects.create(**serializer.validated_data)
            return response_body(data="ok")


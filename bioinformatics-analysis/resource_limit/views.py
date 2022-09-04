from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import psutil
import shutil

from resource_limit.models import ResourceLimit
from resource_limit.serializer import ResourceLimitSerializer
from utils.paginator import PageNumberPaginationWithWrapper
from utils.response import response_body
from django.conf import settings


class ResourceLimitViewSet(ModelViewSet):
    queryset = ResourceLimit.objects.all()
    serializer_class = ResourceLimitSerializer
    pagination_class = PageNumberPaginationWithWrapper

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["creator"] = request.account.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    @action(methods=["GET"], detail=False)
    def resource(self, request, *args, **kwargs):
        mem = psutil.virtual_memory()
        gb = 1024 ** 2
        total_b, used_b, free_b = shutil.disk_usage(settings.TASK_RESULT_DIR)
        return response_body(data={
            "memory": {"all": mem.total // gb, "used": mem.used // gb},
            "disk": {"all": total_b // gb, "used": used_b // gb}
        })




from datetime import datetime

from common.viewsets.viewsets import CustomeViewSets
from utils.response import response_body
from .models import Geneset
from .serializers import GenesetSerializer


class GenesetViewSet(CustomeViewSets):
    queryset = Geneset.objects.filter(del_flag=0)
    serializer_class = GenesetSerializer

    def create(self, request, *args, **kwargs):
        # 创建新记录
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response_body(data=serializer.data, msg="success")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = 1
        instance.deleted_at = datetime.now()
        instance.save()
        return response_body(data=True, msg="success")


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response_body(data=serializer.data, msg="success")



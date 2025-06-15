from datetime import datetime

from rest_framework.decorators import action
from rest_framework.response import Response

from common.viewsets.viewsets import CustomeViewSets
from utils.response import response_body
from .models import Verdict
from .serializers import DiagnosisSerializer


class VerdictViewSet(CustomeViewSets):
    queryset = Verdict.objects.filter(is_deleted=0)
    serializer_class = DiagnosisSerializer

    def create(self, request, *args, **kwargs):
        # 检查是否已存在相同患者和基于标识的记录
        existing = Verdict.objects.filter(
            patient_identifier=request.data.get("patient_identifier"),
            gene_identifier=request.data.get("gene_identifier"),
            is_deleted=0
        ).first()

        if existing:
            # 更新现有记录
            serializer = self.get_serializer(existing, data=request.data, partial=True)
        else:
            # 创建新记录
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response_body(data=serializer.data, msg="success")

    @action(detail=False, methods=["get"])
    def by_patient(self, request):
        patient_identifier = request.query_params.get("patient_identifier")
        if not patient_identifier:
            return Response(response_body(code=1, msg="患者识别号不能为空"))

        queryset = self.get_queryset().filter(patient_identifier=patient_identifier)
        serializer = self.get_serializer(queryset, many=True)
        return response_body(data=serializer.data, msg="success")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = 1
        instance.deleted_at = datetime.now()
        instance.save()
        return response_body(data=True, msg="success")

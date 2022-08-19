from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework import status

from patient.models import Patient
from patient.serializer import PatientSerializer, FileSerializer
from patient.services import file_import as file_import_service
from utils.response import response_body
from utils.paginator import PageNumberPaginationWithWrapper


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = PageNumberPaginationWithWrapper

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["creator"] = request.account.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False)
    def dl_patient_template(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv;charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="patient_template.csv"'
        file_import_service.download_patient_template(response)
        return response

    @action(methods=('POST',), parser_classes=[MultiPartParser], detail=False)
    def import_patients(self, request, *args, **kwargs):
        s = FileSerializer(data=request.data)
        try:
            s.is_valid(raise_exception=True)
            added, existed = file_import_service.import_patients_by_csv(request.account, s.validated_data['file'])
        except Exception as err:
            # middleware attempt to transfer this to utf-8. the middleware should process this case
            request.data["file"] = {}
            return response_body(code=1, msg=str(err))
        return Response(data={"added": added, "existed": existed})



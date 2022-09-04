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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response_body(data={})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_body(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return response_body(data=serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["creator"] = request.account.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response_body(data=serializer.data)

    @action(methods=['get'], detail=False)
    def dl_patient_template(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv;charset=utf-8')
        response[
            'Content-Disposition'] = 'attachment; filename="patient_template.csv"'
        file_import_service.download_patient_template(response)
        return response

    @action(methods=('POST', ), parser_classes=[MultiPartParser], detail=False)
    def import_patients(self, request, *args, **kwargs):
        s = FileSerializer(data=request.data)
        try:
            s.is_valid(raise_exception=True)
            added, existed = file_import_service.import_patients_by_csv(
                request.account, s.validated_data['file'])
        except Exception as err:
            # middleware attempt to transfer this to utf-8. the middleware should process this case
            request.data["file"] = {}
            return response_body(code=1, msg=str(err))
        return response_body(data={"added": added, "existed": existed})

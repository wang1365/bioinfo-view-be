from rest_framework.viewsets import ModelViewSet
import tempfile
import openpyxl
import time
import uuid
from django.db.models import Q

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from account import constants as account_constant

from patient.models import Patient
from patient.serializer import PatientSerializer, FileSerializer
from patient.services import file_import as file_import_service
from utils.response import response_body
from utils.paginator import PageNumberPaginationWithWrapper
from common.filters import CommonFilters
from patient.constant import PATIENT_MODEL_ATTRS
from patient.core import export_to_csv, ExcelHandler, ValueProcess, calculate_age


class PatientFilter(CommonFilters):
    def filter_queryset(self, request, qs, view):
        identifiers = request.GET.get('identifiers')
        if identifiers:
            identifiers = identifiers.split(',')
            con = dict()
            for identifier in identifiers:
                con[f'{identifier}__icontains'] = request.GET.get("search")
            con = Q(**con)
            con.connector = Q.OR
            qs = qs.filter(con)
        return qs


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = PageNumberPaginationWithWrapper
    filter_backends = [PatientFilter]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if account_constant.NORMAL in request.role_list:
            queryset = queryset.filter(creator=request.account)
        elif account_constant.ADMIN in request.role_list:
            queryset = Patient.objects.filter(Q(creator__user2role__role__code=account_constant.NORMAL) | Q(creator=request.account))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=('POST',), parser_classes=[MultiPartParser], detail=False)
    def upload(self, request, suffix=".xlsx"):
        info = {
            "attrs": PATIENT_MODEL_ATTRS,
            "serializer": PatientSerializer
        }
        return self._upload(request, info, suffix)

    def _upload(self, request, info, suffix='.xlsx'):
        up_file = request.FILES['file']

        _, filename = tempfile.mkstemp(suffix=suffix)

        with open(filename, 'wb+') as fp:
            for chunk in up_file.chunks():
                fp.write(chunk)

        excel_handler = ExcelHandler(filename, info['attrs'])
        records = excel_handler.read()

        for record in records:
            record["creator_id"] = request.account.id
            record["identifier"] = str(uuid.uuid4())
            record["birthday"] = record["birthday"].strftime("%Y-%m-%d")

        unsuccessful_records = []
        value_process = ValueProcess(user_id=request.account.id)

        for record in records:
            patient_serializer = info['serializer'](
                data=value_process.process(record))
            if patient_serializer.is_valid():
                patient_serializer.save()
                obj = patient_serializer.instance
                obj.age = calculate_age(obj.birthday)
                obj.identifier = f'P{obj.id:08}'
                obj.save()
            else:
                print(patient_serializer.errors)
                unsuccessful_records.append(record)

        return response_body(data=unsuccessful_records, msg="success")

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
        request.data['creator'] = request.account.id
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
        obj = serializer.instance
        obj.age = calculate_age(obj.birthday)
        obj.identifier = f'P{obj.id:08}'
        obj.save()
        return response_body(data=serializer.data)

    @action(methods=['get'], detail=False)
    def dl_patient_template(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv;charset=utf-8')
        response[
            'Content-Disposition'] = 'attachment; filename="patient_template.csv"'
        file_import_service.download_patient_template(response)
        return response

    @action(methods=['get'], detail=False)
    def template(self, request, *args, **kwargs):
        # response = HttpResponse(content_type='application/ms-excel')
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="patient.xlsx"'
        wb = openpyxl.Workbook()
        # 创建一张新表
        ws = wb.create_sheet(title='患者')
        exclude_keys = ["id", "identifier", "age"]
        columns = [f.get("name") for f in PATIENT_MODEL_ATTRS if f.get(
            "key") not in exclude_keys]
        ws.append(columns)
        wb.save(response)
        return response

    @action(methods=('POST', ), parser_classes=[MultiPartParser], detail=False)
    def import_patients(self, request, *args, **kwargs):
        s = FileSerializer(data=request.data)
        try:
            s.is_valid(raise_exception=True)
            added, existed = file_import_service.import_patients_by_csv(
                request.account, s.validated_data['file'])
        except Exception as err:
            # middleware attempt to transfer this to utf-8. the middleware
            # should process this case
            request.data["file"] = {}
            return response_body(code=1, msg=str(err))
        return response_body(data={"added": added, "existed": existed})

    @action(methods=('GET',), parser_classes=[MultiPartParser], detail=False)
    def export(self, request):
        path = export_to_csv(self.queryset.all())

        with open(path, "rb") as f:
            data = f.read()

        filename = '{}-{}.csv'.format(request.account.username,
                                      int(time.time() * 100))
        response = HttpResponse(data)
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            filename)
        response['Content-Type'] = 'application/octet-stream'
        return response

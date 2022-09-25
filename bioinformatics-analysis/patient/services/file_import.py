
import csv
import logging


from django.db.models import Q
from patient.constant import PATIENT_ZH_TO_EN, PATIENT_MODEL_ATTRS
from rest_framework.exceptions import APIException

from patient.models import Patient


_log = logging.getLogger('patient.services.file_import')


class _FileImporter:
    def __init__(self, user, f):
        self._user = user
        self._f = f
        self.id_card_dict = {}
        self.identifier_index_dict = {}
        self.data_list = []

    def _parse_file(self):
        for index, row in enumerate(csv.DictReader(self._f)):
            id_card = row.get('id_card', '')
            id_card = id_card.strip() if id_card else id_card

            identifier = row.get('identifier', '')
            identifier = identifier.strip() if identifier else identifier

            if not any([id_card, identifier]):
                msg = f'第{index+2}行的身份证号和患者失败号都为空'
                _log.error(msg)
                raise APIException(msg)

            if id_card:
                if id_card in self.id_card_dict:
                    msg = f'第{index + 2}行的身份证号和第{self.id_card_dict[id_card]}行重复'
                    _log.error(msg)
                    raise APIException(msg)
                elif len(id_card) not in [15, 18]:
                    msg = f'第{index+2}行的身份证号不符合长度规范'
                    _log.error(msg)
                    raise APIException(msg)
                else:
                    self.id_card_dict[id_card] = index

            if identifier:
                if identifier in self.identifier_index_dict:
                    msg = f'第{index + 2}行的身份证号和第{self.id_card_dict[id_card]}行重复'
                    _log.error(msg)
                    raise APIException(msg)
                else:
                    self.identifier_index_dict[identifier] = index

            self.data_list.append(row)

    def _make_patient_info(self, row_data):
        return row_data

    def _create_or_update_obj(self):
        processed_index = []

        qs = Patient.objects.all()
        q1 = Q(id_card__in=list(self.id_card_dict.keys()))
        q2 = Q(identifier__in=list(self.identifier_index_dict.keys()))
        qs = qs.filter(q1 | q2)
        for obj in qs:
            if obj.id_card in self.id_card_dict:
                row_data_index = self.id_card_dict[obj.id_card]
            else:
                row_data_index = self.identifier_index_dict[obj.identifier]

            if row_data_index not in processed_index:
                row_data = self.data_list[row_data_index]
                obj_update_dict = self._make_patient_info(row_data)
                for key, val in obj_update_dict.items():
                    setattr(obj, key, val)
                obj.save()
                processed_index.append(row_data_index)

        create_objs = []
        for index, row_data in enumerate(self.data_list):
            if index not in processed_index:
                obj_dict = self._make_patient_info(row_data)
                create_objs.append(Patient(creator=self._user, **obj_dict))
        Patient.objects.bulk_create(create_objs)

        return len(create_objs), len(qs)

    def import_file(self):
        self._parse_file()
        return self._create_or_update_obj()


def import_patients_by_csv(user, f):
    importer = _FileImporter(user, f)
    return importer.import_file()

from openpyxl import load_workbook

def download_patient_template(response):
    load_workbook(response)
    writer = csv.writer(response)
    exclude_keys = ["id", "identifier", "age"]
    writer.writerow([f.get("name") for f in PATIENT_MODEL_ATTRS if f.get("key") not in exclude_keys])

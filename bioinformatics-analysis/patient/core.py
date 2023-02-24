#!/usr/bin/env python3
import csv
import datetime
from datetime import date
import tempfile
import pendulum
from openpyxl import load_workbook
from patient.constant import PATIENT_MODEL_ATTRS

from account.models import Account
from django.core.exceptions import ObjectDoesNotExist


class ExcelHandler:
    def __init__(self, filename, attrs):
        self._filename = filename
        self._index2index = {}
        self._field_names = []
        self._attrs = attrs

    def read(self):
        workbook = load_workbook(self._filename)
        sheet = workbook.active
        # sheet = workbook.get_sheet_by_name("Sheet1")

        result = []

        for index, row_cells in enumerate(sheet.rows):
            if index == 0:
                self._field_names = self._deal_with_headers(row_cells)
            else:
                result.append(self._deal_with_values(row_cells))

        return result

    def _deal_with_headers(self, cells):
        def _compare_name(value):
            return value.replace('\n', '').replace(' ', '').replace('\t', '')
        mappings = {
            attr['name']: index for index,
            attr in enumerate(
                self._attrs)}
        return [
            self._attrs[mappings[_compare_name(cell.value)]]['key']
            for _, cell in enumerate(cells)
        ]

    def _deal_with_values(self, cells):
        values = [cell.value for cell in cells]
        record = dict(zip(self._field_names, values))
        return record


class ValueProcess:
    def __init__(self, user_id=1):
        self._default_user_id = user_id

    def _process_date(self, d):
        if isinstance(d, str):
            return pendulum.parse(d).date()
        if isinstance(d, datetime.datetime):
            return d.date()
        if isinstance(d, datetime.date):
            return d

    def _handle_user(self, username):
        try:
            account = Account.objects.get(username=username)
            return account.id
        except ObjectDoesNotExist:
            return self._default_user_id
        except Exception:
            return self._default_user_id

    def _handle_functions(self):
        return {
            'test_date': self._process_date,
        }

    def _get_function(self, key):
        return self._handle_functions().get(key, lambda x: x)

    def process(self, data):
        return {k: self._get_function(k)(v) for k, v in data.items()}


def export_to_csv(querset):
    headers = [a['name'] for a in PATIENT_MODEL_ATTRS]

    data = [headers]

    for o in querset:
        data.append([getattr(o, a.get('alias', a['key']))
                     for a in PATIENT_MODEL_ATTRS])

    _, filename = tempfile.mkstemp(suffix='.csv')
    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile,
                                delimiter=',',
                                quotechar='\\',
                                quoting=csv.QUOTE_MINIMAL)
        for row in data:
            spamwriter.writerow(row)

    return filename


def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        # raised when birth date is February 29
        # and the current year is not a leap year
        birthday = born.replace(year=today.year, day=born.day - 1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

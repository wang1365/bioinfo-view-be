#!/usr/bin/env python3

from rest_framework import serializers

from patient.serializer import PatientSerializer
from sample.models import Sample, SampleMeta
from sample.constants import SAMPLE_MODEL_ATTRS, SAMPLE_META_MODEL_ATTRS


class SampleMetaSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    # patient_id = serializers.IntegerField(source='patient.id')

    class Meta:
        model = SampleMeta

        fields = ['id', 'patient'] + [f['key'] for f in SAMPLE_META_MODEL_ATTRS]


class SampleSerializer(serializers.ModelSerializer):
    sample_meta = SampleMetaSerializer(read_only=True)
    patient = PatientSerializer(source='sample_meta.patient', read_only=True)

    class Meta:
        model = Sample
        fields = ['id', 'sample_meta', 'patient'] + [f['key'] for f in SAMPLE_MODEL_ATTRS]

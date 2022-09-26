#!/usr/bin/env python3

from rest_framework import serializers

from patient.serializer import PatientSerializer
from sample.models import Sample, SampleMeta
from sample.constants import SAMPLE_MODEL_ATTRS, SAMPLE_META_MODEL_ATTRS

class SampleMetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleMeta

        fields = ['id'] + [f['key'] for f in SAMPLE_META_MODEL_ATTRS]

class SampleSerializer(serializers.ModelSerializer):
    # sample_meta_id = serializers.IntegerField(source='sample_meta.id')
    sample_meta = SampleMetaSerializer(read_only=True)
    patient = PatientSerializer(read_only=True, source='sample_meta.patient_identifier')

    class Meta:
        model = Sample
        # fields = '__all__'
        fields = ['id', 'sample_meta', 'patient'] + [f['key'] for f in SAMPLE_MODEL_ATTRS]



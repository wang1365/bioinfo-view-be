#!/usr/bin/env python3

from rest_framework import serializers

from patient.serializer import PatientSerializer
from sample.models import Sample, SampleMeta
from sample.constants import SAMPLE_MODEL_ATTRS, SAMPLE_META_MODEL_ATTRS


class SampleMetaSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.IntegerField(allow_null=True, default=None)
    patient_identifier = serializers.CharField(allow_null=True, default=None)

    class Meta:
        model = SampleMeta

        fields = ["id", "patient", "patient_id", "identifier", "user", "user_id"] + [
            f["key"] for f in SAMPLE_META_MODEL_ATTRS
        ]


class SampleSerializer(serializers.ModelSerializer):
    sample_meta_id = serializers.IntegerField(allow_null=True, default=None)
    sample_meta = SampleMetaSerializer(read_only=True)
    patient = PatientSerializer(source="sample_meta.patient", read_only=True)
    fastq2_path = serializers.CharField(
        allow_null=True, required=False, default="", allow_blank=True
    )

    class Meta:
        model = Sample
        fields = [
            "id",
            "sample_meta",
            "patient",
            "sample_meta_id",
            "user",
            "user_id",
            "identifier",
        ] + [f["key"] for f in SAMPLE_MODEL_ATTRS]

#!/usr/bin/env python3

from rest_framework import serializers

from sample.models import Sample, SampleMeta
from sample.constants import SAMPLE_MODEL_ATTRS, SAMPLE_META_MODEL_ATTRS


class SampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sample
        fields = ['id'] + [f['key'] for f in SAMPLE_MODEL_ATTRS]

class SampleMetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleMeta

        fields = ['id'] + [f['key'] for f in SAMPLE_META_MODEL_ATTRS]

#!/usr/bin/env python3

from rest_framework import serializers

from sample.models import Sample
from sample.constants import MODEL_ATTRS


class SampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sample
        fields = ['id'] + [f['key'] for f in MODEL_ATTRS] + [
            'real_fastq1_path',
            'real_fastq2_path',
            'real_bam1_path',
            'real_bam2_path',
            'task_id',
            'username',
            'is_standard',
        ]

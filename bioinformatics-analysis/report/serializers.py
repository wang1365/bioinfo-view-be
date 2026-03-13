#!/usr/bin/env python3

from rest_framework import serializers

from report.models import Report
from task.serializers import TaskSerializer


class ReportSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    sample_id = serializers.IntegerField(source='sample.id', read_only=True, allow_null=True)


    class Meta:
        model = Report
        fields = ['id', 'task', 'creator_id', 'comment', 'task_id', 'query', 'sample_id', 'report_path_cn', 'report_path_en', 'status', 'create_time']

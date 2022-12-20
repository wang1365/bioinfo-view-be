#!/usr/bin/env python3

from rest_framework import serializers

from report.models import Report
from task.serializers import TaskSerializer


class ReportSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'task', 'creator_id', 'comment', 'task_id', 'query']

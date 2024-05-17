from rest_framework import serializers

from account.serializer import AccountSerializer
from project.serializer import ProjectSerializer
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    project = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"
        depth = 1

    def get_project(self, obj):
        return ProjectSerializer(obj.project).data

    def get_creator(self, obj):
        return AccountSerializer(obj.creator).data


class ListTaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = Task
        fields = [
            "project",
            "creator",
            "id",
            "progress",
            "samples",
            "name",
            "status",
            "is_merge",
            "flow",
            "result_path",
            "result_path_CN",
            "result_path_EN",
            "is_qc",
            "env",
            "priority",
            "error_message",
            "error_message_EN",
            "error_message_CN",
            "create_time",
            # "create_time_timestamp",
            "log",
            "deleted_tempdir",
        ]

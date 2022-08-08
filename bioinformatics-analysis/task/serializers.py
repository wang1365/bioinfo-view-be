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
            "name",
            "status",
            "is_merge",
            "flow",
            "result_path",
            "is_qc",
            "env",
            "priority",
            "create_time"
        ]

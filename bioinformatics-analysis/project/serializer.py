from rest_framework import serializers

from project.models import Project, ProjectMembers
from task.models import Task


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username")
    owner_id = serializers.CharField(source="owner.id")
    members = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "desc",
            # "code",
            "owner",
            "samples",
            "owner_id",
            "members",
            "task_count",
            "create_time",
        ]

    def get_members(self, obj):
        return [
            {
                "id": i.id,
                "username": i.username,
                "email": i.email,
                "department": i.department,
                "create_time": ProjectMembers.objects.filter(account=i, project=obj)
                .first()
                .create_time,
            }
            for i in obj.members.all()
        ]

    def get_task_count(self, obj):
        return Task.objects.filter(project=obj).count()

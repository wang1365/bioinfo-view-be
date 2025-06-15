from rest_framework import serializers
from .models import Verdict

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verdict
        fields = "__all__"
        read_only_fields = ("created_at", "is_deleted", "deleted_at")

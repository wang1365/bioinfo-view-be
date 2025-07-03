from rest_framework import serializers
from .models import Geneset

class GenesetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geneset
        fields = "__all__"
        read_only_fields = ("created_at", "del_flag")

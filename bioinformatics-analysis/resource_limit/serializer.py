import mimetypes
import io

from rest_framework import serializers

from resource_limit.models import ResourceLimit


class ResourceLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceLimit
        fields = '__all__'
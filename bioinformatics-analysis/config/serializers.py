#!/usr/bin/env python3
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from config.models import Config, Resource


class ConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = Config
        fields = ['id', 'name', 'value', 'used']

class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = "__all__"
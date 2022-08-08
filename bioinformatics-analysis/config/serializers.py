#!/usr/bin/env python3
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from config.models import Config


class ConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = Config
        fields = ['id', 'name', 'value']

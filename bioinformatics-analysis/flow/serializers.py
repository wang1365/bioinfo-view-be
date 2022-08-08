#!/usr/bin/env python3
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from flow.models import Flow


class FlowSerializer(serializers.ModelSerializer):
    def validate_type(self, tp, **params):
        if tp not in ['array', 'string', 'number', 'boolean', 'file']:
            raise ValidationError('不支持该 {} 类型'.format(tp))
        return tp

    def validate_code(self, code, **params):
        if not code.isalnum():
            raise ValidationError("{} 中包含非法字符".format(code))
        return code

    class Meta:
        model = Flow
        fields = [
            "id", "name", "code", "desp", "owner_id", "alignment_tool",
            "parameter_schema", "flow_category", "flow_type", "sample_type",
            "details", "parameters", "location", "memory",
            "builtin_parameters", "create_time", "allow_nonstandard_samples",
        ]

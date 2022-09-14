#!/usr/bin/env python3
from shutil import ExecError
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from flow.models import Flow
from flow.core import load_image
import os


class FlowSerializer(serializers.ModelSerializer):
    def validate_type(self, tp, **params):
        if tp not in ['array', 'string', 'number', 'boolean', 'file']:
            raise ValidationError('不支持该 {} 类型'.format(tp))
        return tp

    def validate_code(self, code, **params):
        if not code.isalnum():
            raise ValidationError("{} 中包含非法字符".format(code))
        return code

    def validate_tar_path(self, tar_path, **params):
        real_tar_path = tar_path
        if not tar_path.startswith("/"):
            real_tar_path = os.path.join("/data/bioinfo/image_dir", tar_path)

        if not os.getenv('FLOW_DOCKER_VALIDATE'):
            return real_tar_path
        try:
            load_image(real_tar_path, self.initial_data['image_name'])
        except Exception:
            raise ValidationError("无法加载镜像")
        return real_tar_path

    class Meta:
        model = Flow
        fields = [
            "id", "name", "code", "desp", "owner_id", "alignment_tool",
            "parameter_schema", "flow_category", "flow_type", "sample_type",
            "details", "parameters", "memory", "tar_path", "image_name",
            "builtin_parameters", "create_time", "allow_nonstandard_samples",
        ]

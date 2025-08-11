from rest_framework import serializers
from .models import ReferenceGenome


class ReferenceGenomeSerializer(serializers.ModelSerializer):
    """自建参考基因组序列化器"""
    
    class Meta:
        model = ReferenceGenome
        fields = [
            'id',
            'custom_database',
            'virus_name',
            'virus_type',
            'host',
            'host_genome_version',
            'host_seq_file',
            'virus_seq_file',
            'host_map_db',
            'sp_map_db',
            'create_time',
            'update_time',
            'is_deleted'
        ]
        read_only_fields = ['id', 'create_time', 'update_time']

    def validate_custom_database(self, value):
        """验证自定义数据库名"""
        if not value or not value.strip():
            raise serializers.ValidationError("自定义数据库名不能为空")
        return value.strip()

    def validate_host(self, value):
        """验证宿主信息"""
        if not value or not value.strip():
            raise serializers.ValidationError("宿主信息不能为空")
        return value.strip()

    def validate_host_genome_version(self, value):
        """验证宿主基因组版本"""
        if not value or not value.strip():
            raise serializers.ValidationError("宿主基因组版本不能为空")
        return value.strip()

    # def validate_host_seq_file(self, value):
    #     """验证宿主原序列文件路径"""
    #     if not value or not value.strip():
    #         raise serializers.ValidationError("宿主原序列文件路径不能为空")
    #     return value.strip()

    # def validate_virus_seq_file(self, value):
    #     """验证病原原序列文件路径"""
    #     if not value or not value.strip():
    #         raise serializers.ValidationError("病原原序列文件路径不能为空")
    #     return value.strip()


class ReferenceGenomeCreateSerializer(ReferenceGenomeSerializer):
    """创建自建参考基因组的序列化器"""
    
    class Meta(ReferenceGenomeSerializer.Meta):
        fields = [
            'custom_database',
            'virus_name',
            'virus_type',
            'host',
            'host_genome_version',
            'host_seq_file',
            'virus_seq_file',
            'host_map_db',
            'sp_map_db'
        ]


class ReferenceGenomeListSerializer(serializers.ModelSerializer):
    """自建参考基因组列表序列化器（简化版）"""
    
    class Meta:
        model = ReferenceGenome
        fields = [
            'id',
            'custom_database',
            'host',
            'host_genome_version',
            'virus_name',
            'virus_type',
            'create_time',
            'update_time'
        ]
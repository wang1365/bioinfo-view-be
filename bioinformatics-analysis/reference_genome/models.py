from django.db import models
from django.utils.timezone import now
from account.models import Account


class ReferenceGenome(models.Model):
    """自建参考基因组模型"""
    
    # 自定义数据库名
    custom_database = models.CharField(
        max_length=255, 
        verbose_name="自定义数据库名",
        help_text="自定义数据库名称"
    )
    
    # 病毒种名 - 使用JSONField存储
    virus_name = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name="病毒种名",
        help_text="病毒种名信息，JSON格式"
    )
    
    # 病毒分型 - 使用JSONField存储
    virus_type = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name="病毒分型",
        help_text="病毒分型信息，JSON格式"
    )
    
    # 宿主
    host = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="宿主",
        help_text="宿主信息"
    )
    
    # 宿主基因组版本
    host_genome_version = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="宿主基因组版本",
        help_text="宿主基因组版本信息"
    )
    
    # 宿主原序列文件
    host_seq_file = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="宿主原序列文件",
        help_text="宿主原序列文件路径"
    )
    
    # 病原原序列文件
    virus_seq_file = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="病原原序列文件",
        help_text="病原原序列文件路径"
    )
    
    # 宿主原序列信息 - 使用JSONField存储
    host_map_db = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name="宿主原序列信息",
        help_text="宿主原序列详细信息，JSON格式"
    )
    
    # 病原原序列信息 - 使用JSONField存储
    sp_map_db = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name="病原原序列信息",
        help_text="病原原序列详细信息，JSON格式"
    )
    
    # 创建时间
    create_time = models.DateTimeField(
        "创建时间", 
        default=now
    )
    
    # 更新时间
    update_time = models.DateTimeField(
        "修改时间", 
        auto_now=True
    )
    
    # 删除标识
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="删除标识",
        help_text="软删除标识，True表示已删除"
    )
    
    # 状态字段
    status = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default="RUNNING",
        verbose_name="状态",
        help_text="参考基因组状态"
    )
    
    # 消息字段
    message = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name="消息",
        help_text="相关消息信息，JSON格式"
    )

    class Meta:
        verbose_name = "自建参考基因组"
        verbose_name_plural = "自建参考基因组"
        db_table = "reference_genome"
        ordering = ['-create_time']

    def __str__(self):
        return f"{self.custom_database} - {self.host}"

    def soft_delete(self):
        """软删除方法"""
        self.is_deleted = True
        self.save()

    @classmethod
    def get_active_objects(cls):
        """获取未删除的对象"""
        return cls.objects.filter(is_deleted=False)
from django.db import models
import json

class Verdict(models.Model):
    patient_identifier = models.CharField(max_length=100, null=True, verbose_name="患者识别号")
    gene_identifier = models.CharField(max_length=100, null=True, verbose_name="基因标识")
    result = models.JSONField(default=list, null=True, verbose_name="诊断结果")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_deleted = models.SmallIntegerField(default=0, verbose_name="删除标识")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="删除时间")

    class Meta:
        db_table = "verdict"
        verbose_name = "用户诊断"
        verbose_name_plural = verbose_name
        unique_together = ("patient_identifier", "gene_identifier")

    def __str__(self):
        return f"{self.patient_identifier}-{self.gene_identifier}"

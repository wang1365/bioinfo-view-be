from django.db import models
import json

class Geneset(models.Model):
    user_id = models.IntegerField(max_length=100, null=True, verbose_name="用户名")
    geneset = models.JSONField(default=list, null=True, verbose_name="geneset")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    del_flag = models.IntegerField(default=0, verbose_name="删除标识")

    class Meta:
        db_table = "geneset"
        verbose_name = "Geneset"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.username}-{self.geneset}"

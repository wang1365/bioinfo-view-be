import json

from django.db import models
from django.utils.timezone import now

from account.models import Account
from flow.constants import BUILTIN_PARAMETER_SCHEMA


class Flow(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)
    code = models.CharField(max_length=128, blank=True, unique=True)

    desp = models.TextField(blank=True, default='')

    owner_id = models.BigIntegerField(default=-1)

    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", default=now)

    # 生信脚本地址
    location = models.CharField(max_length=100, blank=False, unique=True)

    # 比对软件
    alignment_tool = models.CharField(max_length=64)

    parameter_schema = models.TextField()

    memory = models.BigIntegerField(default=1024)  # 单位 MB

    # 样本类型多少：single, double, multiple
    sample_type = models.CharField(
        max_length=64, blank=True, default="multiple"
    )

    flow_type = models.CharField(max_length=64, blank=True, default="normal")

    flow_category = models.CharField(max_length=64, blank=True, default='')

    allow_nonstandard_samples = models.BooleanField(default=False)

    members = models.ManyToManyField(to=Account,
                                     through="FlowMembers",
                                     related_name="join_flows")

    details = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "flow"
        ordering = ["-id"]
        get_latest_by = "id"

    @property
    def parameters(self):
        return json.loads(self.parameter_schema)

    @property
    def builtin_parameters(self):
        return BUILTIN_PARAMETER_SCHEMA

    @classmethod
    def qc_task(self, alignment_tool='bwa'):
        try:
            return self.objects.get(
                alignment_tool=alignment_tool, flow_type='qc')
        except Exception:
            return None


class Flow2Sample(models.Model):
    flow_id = models.BigIntegerField()
    sample_id = models.BigIntegerField()
    task_id = models.BigIntegerField()
    project_id = models.BigIntegerField()
    filepath = models.CharField(max_length=256)

    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        db_table = "flow_samples"
        ordering = ["-id"]
        verbose_name = "流程样本表"
        verbose_name_plural = verbose_name
        get_latest_by = "id"


class FlowMembers(models.Model):
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    flow = models.ForeignKey(to=Flow, on_delete=models.CASCADE)
    create_time = models.DateTimeField("创建时间", default=now)

    class Meta:
        unique_together = ('account', 'flow')
        db_table = "flow_members"
        ordering = ["-id"]
        verbose_name = "流程的权限分配表"
        verbose_name_plural = verbose_name
        get_latest_by = "id"

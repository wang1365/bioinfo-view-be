# Create your models here.
import os

from django.db import models
from django.utils.timezone import now

# from django_mysql.models import JSONField
from sample.models import Sample

from django.db.models import JSONField

from account.models import Account
from flow.models import Flow
from project.models import Project


class Task(models.Model):
    name = models.CharField(max_length=100, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status_choices = (
        (1, "PENDING"),
        (2, "RUNNING"),
        (3, "FINISHED"),
        (4, "FAILURED"),
        (5, "CANCELED"),
    )
    status = models.SmallIntegerField(choices=status_choices, default=1)
    progress = models.SmallIntegerField(default=0)
    creator = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    pid = models.CharField(max_length=256, blank=True, null=True)
    is_merge = models.BooleanField(default=False)  # 是否归并任务结果
    flow = models.ForeignKey(to=Flow, on_delete=models.CASCADE)
    result_path = models.TextField(null=True)
    result_path_CN = models.TextField(null=True)
    result_path_EN = models.TextField(null=True)
    result_dir = models.CharField(max_length=120, null=True)
    keep_bam = models.BooleanField(default=False)
    has_cleaned = models.BooleanField(default=False)
    is_qc = models.BooleanField(default=False)
    env = JSONField(blank=True, null=True, default=dict)
    priority = models.SmallIntegerField(default=1)
    memory = models.BigIntegerField()  # 单位MB
    samples = JSONField()
    log = models.TextField(null=True)
    parameter = JSONField(null=True)
    error_message = models.TextField(null=True, default="")
    error_message_EN = models.TextField(null=True, default="")
    error_message_CN = models.TextField(null=True, default="")
    create_time = models.DateTimeField("创建时间", default=now)
    # TODO on_update
    update_time = models.DateTimeField("修改时间", auto_now=True)
    deleted_tempdir = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "task"
        ordering = ["-id"]
        verbose_name = "任务"
        verbose_name_plural = verbose_name
        get_latest_by = "id"


class TaskSample(models.Model):
    task = models.ForeignKey(
        Task, related_name="task_samples", on_delete=models.CASCADE
    )
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        db_table = "task_sample"
        ordering = ["-id"]

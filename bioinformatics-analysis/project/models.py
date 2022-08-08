from django.db import models
import string
import re
from django.core.exceptions import ValidationError

from django.utils.timezone import now
from django.core.validators import RegexValidator
from account.models import Account
from sample.models import Sample

# from django_mysql.models import JSONField


# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=256, null=False)
    # code = models.CharField(max_length=256, null=True, default=None)
    desc = models.TextField(default="")
    owner = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name="projects"
    )
    is_visible = models.BooleanField(default=True)
    is_builtin = models.BooleanField(default=False)
    samples = models.ManyToManyField(to=Sample)
    members = models.ManyToManyField(to=Account,
                                     through="ProjectMembers",
                                     related_name="join_projects")
    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "project"
        ordering = ["-id"]
        verbose_name = "项目"
        verbose_name_plural = verbose_name
        get_latest_by = "id"


    # def save(self, *args, **kwargs):
    #     if not self.code.isalnum() or re.findall('[\u4e00-\u9fa5]', self.code):
    #         raise ValidationError('项目编码只能由大小写英文字母组成')
    #     try:
    #         self.full_clean()
    #         super().save(*args, **kwargs)
    #     except ValidationError as e:
    #         raise ValidationError(e)

class ProjectMembers(models.Model):
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    create_time = models.DateTimeField("创建时间", default=now)

    class Meta:
        db_table = "project_members"
        ordering = ["-id"]
        verbose_name = "项目成员表"
        verbose_name_plural = verbose_name
        get_latest_by = "id"

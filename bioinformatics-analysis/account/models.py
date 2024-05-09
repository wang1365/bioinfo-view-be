from django.db import models
from django.utils.timezone import now

# Create your models here.


class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=100, default='')
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=256)
    department = models.CharField(max_length=128, null=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    disk_limit = models.BigIntegerField(null=True, blank=True, default=0)  # MB
    parent = models.ForeignKey(to="self", null=True, blank=True, on_delete=models.DO_NOTHING)
    used_disk = models.PositiveBigIntegerField(default=0)   # MB
    task_limit = models.BigIntegerField(null=True, blank=True)
    task_count = models.BigIntegerField(default=0)
    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "account"
        ordering = ["id"]
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        get_latest_by = "id"

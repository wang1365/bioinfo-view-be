from django.db import models
from django.utils.timezone import now

# Create your models here.


class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=256)
    department = models.CharField(max_length=128, null=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
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

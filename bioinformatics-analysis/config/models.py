from django.db import models

# Create your models here.


class Config(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)
    value = models.FloatField(default=0, null=True)
    used = models.FloatField(default=0, null=True, blank=True)

    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("修改时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "config"
        ordering = ["-id"]
        get_latest_by = "id"


class Resource(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    value = models.FloatField(default=0, null=True)
    typ = models.CharField(max_length=24)
    day = models.DateField()
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        db_table = "resource"
        ordering = ["-id"]
        get_latest_by = "id"
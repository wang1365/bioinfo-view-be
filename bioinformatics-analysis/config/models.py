from django.db import models

# Create your models here.
class Config(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)
    value = models.FloatField(default=0, null=True)

    create_time = models.DateTimeField("创建时间", auto_created=True)
    update_time = models.DateTimeField("修改时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "config"
        ordering = ["-id"]
        get_latest_by = "id"

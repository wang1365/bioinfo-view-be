from django.db import models
from django.utils.timezone import now

# Create your models here.

class SiteLayOut(models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField(upload_to="media")
    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", auto_now=True)

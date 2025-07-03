from django.db import models
from django.utils import timezone

class Cohort(models.Model):
    ref_gene = models.CharField(max_length=255, default="")
    chr = models.CharField(max_length=50, default="")
    chr_start = models.CharField(max_length=50, default="")
    chr_end = models.CharField(max_length=50, default="")
    ref = models.CharField(max_length=255, default="")
    alt = models.CharField(max_length=255, default="")
    count = models.IntegerField(default=0)
    panel = models.CharField(max_length=255, default="")
    task_id = models.IntegerField(null=True)
    user_id = models.IntegerField()
    create_time = models.DateTimeField(default=timezone.now)
    del_flag = models.IntegerField(default=0)

    class Meta:
        db_table = 'cohort'

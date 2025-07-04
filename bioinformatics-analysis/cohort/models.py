from django.db import models
from django.utils import timezone

class Cohort(models.Model):
    gene_info = models.CharField(max_length=255, default="")
    panel_id = models.IntegerField()
    task_id = models.IntegerField()
    user_id = models.IntegerField()
    create_time = models.DateTimeField(default=timezone.now)
    del_flag = models.IntegerField(default=0)

    class Meta:
        db_table = 'cohort'

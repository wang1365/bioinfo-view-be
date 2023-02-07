from django.db import models
from django.utils.timezone import now

from task.models import Task
from account.models import Account
from django.db.models import DO_NOTHING

# Create your models here.


class Report(models.Model):
    task = models.ForeignKey(to=Task,
                             db_constraint=False,
                             default=None,
                             on_delete=DO_NOTHING)

    #script = models.CharField(max_length=512,null=True)

    creator = models.ForeignKey(to=Account, on_delete=models.CASCADE)

    query = models.TextField()
    comment = models.TextField(null=True)
    report_path = models.TextField(null=True)
    create_time = models.DateTimeField(default=now,null=True)
    status = models.CharField(max_length=32,null=True)

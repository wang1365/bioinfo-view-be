

from django.utils.timezone import now
from django.db import models

from account.models import Account


class ResourceLimit(models.Model):
    DISK = 'disk'
    MEMORY = 'memory'
    LimitType = (
        (DISK, 'disk'),
        (MEMORY, 'memory'),
    )

    user = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name="resource_limit")
    creator = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name="resource_limits")
    limit = models.PositiveIntegerField(default=0)  # unit MB
    limit_type = models.CharField(max_length=24, choices=LimitType, default=DISK)
    desc = models.TextField(default="")
    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", auto_now=True)

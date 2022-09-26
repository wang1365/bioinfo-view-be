from django.core.management.base import BaseCommand

from account.models import Account
from rbac.models import Role, User2Role
from utils.site import get_md5
from config.models import Config
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'init config'

    def handle(self, *args, **options):
        if not Config.objects.filter(name="max_task").exists():
            Config.objects.create(name="max_task", value=10, create_time=now(), update_time=now())
        if not Config.objects.filter(name="memory_rate").exists():
            Config.objects.create(name="memory_rate", value=0.8, create_time=now(), update_time=now())
        if not Config.objects.filter(name="disk").exists():
            # MB
            Config.objects.create(name="disk", value=20 * 1024, create_time=now(), update_time=now())

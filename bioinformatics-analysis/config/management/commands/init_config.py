from django.core.management.base import BaseCommand

from account.models import Account
from rbac.models import Role, User2Role
from utils.site import get_md5
from config.models import Config
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'init config'

    def handle(self, *args, **options):
        Config.objects.all().delete()
        Config.objects.bulk_create([
            Config(name="max_task", value=10, create_time=now(), update_time=now()),
            Config(name="memory_rate", value=10000, create_time=now(), update_time=now()),
        ])

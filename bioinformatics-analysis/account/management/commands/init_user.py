from django.core.management.base import BaseCommand

from account.models import Account
from rbac.models import Role, User2Role
from utils.site import get_md5


class Command(BaseCommand):
    help = 'init user account'

    def handle(self, *args, **options):
        Role.objects.all().delete()
        Role.objects.bulk_create([
            Role(code="super"),
            Role(code="admin"),
            Role(code="normal"),
        ])
        super_role = Role.objects.get(code="super")
        admin_role = Role.objects.get(code="admin")
        super_account, _ = Account.objects.update_or_create(
            defaults={'username': "super", 'nickname': '超级管理员', 'password': get_md5("1234qwer"), 'is_active': True},
            email="super@super.com")
        admin_account, _ = Account.objects.update_or_create(
            defaults={'username': "admin", 'nickname': '管理员', 'password': get_md5("1234qwer"), 'is_active': True},
            email="admin@admin.com")
        User2Role.objects.update_or_create(user=super_account, role=super_role)
        User2Role.objects.update_or_create(user=admin_account, role=admin_role)

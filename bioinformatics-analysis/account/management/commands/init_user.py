from django.core.management.base import BaseCommand

from account.models import Account
from rbac.models import Role, User2Role
from utils.site import get_md5


class Command(BaseCommand):
    help = 'init user account'

    def create_role(self, code):
        if not Role.objects.filter(code=code).exists():
            Role.objects.create(Role(code=code))

    def handle(self, *args, **options):
        self.create_role("super")
        self.create_role("admin")
        self.create_role("normal")

        super_role = Role.objects.get(code="super")
        admin_role = Role.objects.get(code="admin")

        super_account, _ = Account.objects.update_or_create(
            defaults={'username': "super", 'nickname': '超级管理员', 'password': get_md5("1234qwer"), 'is_active': True},
            email="super@super.com")
        User2Role.objects.update_or_create(user=super_account, role=super_role)

        admin_account, _ = Account.objects.update_or_create(
            defaults={'username': "admin", 'nickname': '管理员', 'password': get_md5("1234qwer"), 'is_active': True},
            email="admin@admin.com")
        User2Role.objects.update_or_create(user=admin_account, role=admin_role)

from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id",
                  "username",
                  "email",
                  "is_active",
                  "department",
                  "password",
                  "nickname",
                  "disk_limit",
                  "used_disk",
                  "task_limit",
                  "task_count"
                  ]


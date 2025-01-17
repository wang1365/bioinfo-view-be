# Generated by Django 3.2.3 on 2023-05-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_account_disk_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='task_count',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='task_limit',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]

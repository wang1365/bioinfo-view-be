# Generated by Django 3.2.3 on 2023-03-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='disk_limit',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
    ]

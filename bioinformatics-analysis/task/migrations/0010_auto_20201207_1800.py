# Generated by Django 2.1 on 2020-12-07 18:00

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_auto_20201201_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='parameter',
            field=django_mysql.models.JSONField(default=dict, null=True),
        ),
    ]

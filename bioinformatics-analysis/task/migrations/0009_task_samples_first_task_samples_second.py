# Generated by Django 4.1 on 2024-07-23 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_auto_20230505_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='samples_first',
            field=models.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='task',
            name='samples_second',
            field=models.JSONField(default=[]),
        ),
    ]

# Generated by Django 2.1 on 2020-11-13 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20201029_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.SmallIntegerField(default=0),
        ),
    ]

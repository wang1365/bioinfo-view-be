# Generated by Django 2.1 on 2020-12-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0010_auto_20201204_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='code',
            field=models.CharField(blank=True, max_length=128, unique=True),
        ),
    ]

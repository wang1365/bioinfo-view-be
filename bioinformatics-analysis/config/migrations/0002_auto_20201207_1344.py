# Generated by Django 2.1 on 2020-12-07 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='value',
            field=models.FloatField(default=0, null=True),
        ),
    ]

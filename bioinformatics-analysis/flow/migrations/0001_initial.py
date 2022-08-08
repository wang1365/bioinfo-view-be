# Generated by Django 2.1 on 2020-10-19 14:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, unique=True)),
                ('desp', models.TextField()),
                ('owner_id', models.BigIntegerField(default=-1)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
                ('location', models.CharField(max_length=100, unique=True)),
                ('alignment_tool', models.CharField(max_length=64)),
                ('parameter_schema', models.TextField()),
            ],
            options={
                'db_table': 'flow',
                'ordering': ['-id'],
                'get_latest_by': 'id',
            },
        ),
    ]

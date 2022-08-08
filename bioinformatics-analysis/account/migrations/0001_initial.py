# Generated by Django 2.1 on 2020-10-19 14:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('is_active', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'account',
                'ordering': ['id'],
                'get_latest_by': 'id',
            },
        ),
    ]

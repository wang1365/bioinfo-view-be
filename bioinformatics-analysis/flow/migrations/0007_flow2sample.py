# Generated by Django 2.1 on 2020-12-01 14:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0006_flow_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flow2Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_id', models.BigIntegerField()),
                ('sample_id', models.BigIntegerField()),
                ('task_id', models.BigIntegerField()),
                ('filepath', models.CharField(max_length=256)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
    ]

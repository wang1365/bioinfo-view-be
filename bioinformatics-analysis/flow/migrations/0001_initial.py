# Generated by Django 4.1 on 2022-09-05 20:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, unique=True)),
                ('code', models.CharField(blank=True, max_length=128, unique=True)),
                ('desp', models.TextField(blank=True, default='')),
                ('owner_id', models.BigIntegerField(default=-1)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
                ('location', models.CharField(max_length=100, unique=True)),
                ('alignment_tool', models.CharField(max_length=64)),
                ('parameter_schema', models.TextField()),
                ('memory', models.BigIntegerField(default=1024)),
                ('sample_type', models.CharField(blank=True, default='multiple', max_length=64)),
                ('flow_type', models.CharField(blank=True, default='normal', max_length=64)),
                ('flow_category', models.CharField(blank=True, default='', max_length=64)),
                ('allow_nonstandard_samples', models.BooleanField(default=False)),
                ('details', models.TextField(blank=True, default='')),
            ],
            options={
                'db_table': 'flow',
                'ordering': ['-id'],
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Flow2Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_id', models.BigIntegerField()),
                ('sample_id', models.BigIntegerField()),
                ('task_id', models.BigIntegerField()),
                ('project_id', models.BigIntegerField()),
                ('filepath', models.CharField(max_length=256)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '流程样本表',
                'verbose_name_plural': '流程样本表',
                'db_table': 'flow_samples',
                'ordering': ['-id'],
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='FlowMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flow.flow')),
            ],
            options={
                'verbose_name': '流程的权限分配表',
                'verbose_name_plural': '流程的权限分配表',
                'db_table': 'flow_members',
                'ordering': ['-id'],
                'get_latest_by': 'id',
                'unique_together': {('account', 'flow')},
            },
        ),
        migrations.AddField(
            model_name='flow',
            name='members',
            field=models.ManyToManyField(related_name='join_flows', through='flow.FlowMembers', to='account.account'),
        ),
    ]

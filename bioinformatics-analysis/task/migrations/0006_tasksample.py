# Generated by Django 3.2.3 on 2023-03-11 09:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0003_remove_sample_user_id_remove_samplemeta_user_id_and_more'),
        ('task', '0005_task_deleted_tempdir'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.sample')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_samples', to='task.task')),
            ],
            options={
                'db_table': 'task_sample',
                'ordering': ['-id'],
            },
        ),
    ]

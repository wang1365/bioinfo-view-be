# Generated by Django 4.1 on 2022-09-07 22:18

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
            name='ResourceLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.PositiveIntegerField(default=0)),
                ('limit_type', models.CharField(choices=[('disk', 'disk'), ('memory', 'memory')], default='disk', max_length=24)),
                ('desc', models.TextField(default='')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_limits', to='account.account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_limit', to='account.account')),
            ],
        ),
    ]

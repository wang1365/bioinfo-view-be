# Generated by Django 3.2.3 on 2022-09-17 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='prognosis_time',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='recurrence_time',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='survival_time',
        ),
    ]
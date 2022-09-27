# Generated by Django 3.2.3 on 2022-09-21 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20220917_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='prognosis_time',
        ),
        migrations.AddField(
            model_name='patient',
            name='blood_type',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='diagnosis_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='patient',
            name='drinking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='prognosis',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='smoking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='viral_infection',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
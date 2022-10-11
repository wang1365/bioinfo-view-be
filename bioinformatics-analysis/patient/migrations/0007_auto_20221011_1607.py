# Generated by Django 3.2.3 on 2022-10-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_alter_patient_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='prognosis_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
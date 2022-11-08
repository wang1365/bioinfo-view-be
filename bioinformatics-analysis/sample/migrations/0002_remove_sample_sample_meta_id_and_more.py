# Generated by Django 4.1 on 2022-11-08 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_auto_20221011_1607'),
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='sample_meta_id',
        ),
        migrations.RemoveField(
            model_name='samplemeta',
            name='patient_id',
        ),
        migrations.AddField(
            model_name='sample',
            name='sample_meta',
            field=models.ForeignKey(db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sample.samplemeta'),
        ),
        migrations.AddField(
            model_name='samplemeta',
            name='patient',
            field=models.ForeignKey(db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patient.patient'),
        ),
        migrations.AlterField(
            model_name='samplemeta',
            name='patient_identifier',
            field=models.CharField(max_length=256, null=True),
        ),
    ]

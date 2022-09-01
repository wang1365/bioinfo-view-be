# Generated by Django 4.1 on 2022-09-01 21:12

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
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveSmallIntegerField()),
                ('birthday', models.DateField()),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('id_card', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('medical_doctor', models.CharField(blank=True, max_length=128, null=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('unknown', 'unknown')], max_length=12)),
                ('location', models.CharField(blank=True, max_length=256, null=True)),
                ('identifier', models.CharField(max_length=256, unique=True)),
                ('inspection_agency', models.CharField(blank=True, max_length=256, null=True)),
                ('tumor_stage', models.CharField(blank=True, max_length=256, null=True)),
                ('diagnosis', models.CharField(blank=True, max_length=256, null=True)),
                ('disease', models.CharField(blank=True, max_length=256, null=True)),
                ('family_history', models.CharField(blank=True, max_length=256, null=True)),
                ('medication_history', models.CharField(blank=True, max_length=256, null=True)),
                ('treatment_history', models.CharField(blank=True, max_length=256, null=True)),
                ('prognosis_time', models.DateTimeField(blank=True, null=True)),
                ('recurrence_time', models.DateTimeField(blank=True, null=True)),
                ('survival_time', models.DateTimeField(blank=True, null=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
        ),
    ]

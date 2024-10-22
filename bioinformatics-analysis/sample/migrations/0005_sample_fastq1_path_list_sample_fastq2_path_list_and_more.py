# Generated by Django 4.1 on 2024-09-08 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0004_alter_sample_fastq2_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='fastq1_path_list',
            field=models.CharField(default='', max_length=1024, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='fastq2_path_list',
            field=models.CharField(default='', max_length=1024, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='fastq_merge_required',
            field=models.BooleanField(default=False),
        ),
    ]

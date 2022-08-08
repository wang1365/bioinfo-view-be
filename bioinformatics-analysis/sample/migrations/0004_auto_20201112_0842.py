# Generated by Django 2.1 on 2020-11-12 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0003_auto_20201111_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='barocode_1',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='sample',
            name='barocode_2',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='sample',
            name='company',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='sample',
            name='platform',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='sample',
            name='quality_30',
            field=models.DecimalField(decimal_places=2, default=-1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sample',
            name='real_size',
            field=models.DecimalField(decimal_places=2, default=-1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sequence_size',
            field=models.DecimalField(decimal_places=2, default=-1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sample',
            name='test_type',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0009_task_samples_first_task_samples_second"),
    ]

    operations = [
        migrations.AddField(
            model_name="tasksample",
            name="active_report_type",
            field=models.CharField(blank=True, default="default", max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="tasksample",
            name="custom_report_path_cn",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tasksample",
            name="custom_report_path_en",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tasksample",
            name="custom_report_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

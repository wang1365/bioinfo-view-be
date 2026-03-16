from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sample", "0005_sample_fastq1_path_list_sample_fastq2_path_list_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="samplemeta",
            name="is_nc_sample",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="samplemeta",
            name="tag_label",
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]

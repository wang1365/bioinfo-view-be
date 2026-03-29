from django.db import migrations, models


def forwards_copy_tag_label(apps, schema_editor):
    SampleMeta = apps.get_model('sample', 'SampleMeta')
    SampleData = apps.get_model('sample', 'SampleData')

    meta_tag_map = {
        item['id']: item['tag_label']
        for item in SampleMeta.objects.exclude(tag_label__isnull=True).exclude(tag_label='').values('id', 'tag_label')
    }
    if not meta_tag_map:
        return

    for sample in SampleData.objects.all().iterator():
        tag_label = meta_tag_map.get(sample.sample_meta_id)
        if tag_label is None:
            continue
        sample.tag_label = tag_label
        sample.save(update_fields=['tag_label'])


def backwards_copy_tag_label(apps, schema_editor):
    SampleMeta = apps.get_model('sample', 'SampleMeta')
    SampleData = apps.get_model('sample', 'SampleData')

    meta_updates = {}
    for sample in SampleData.objects.exclude(tag_label__isnull=True).exclude(tag_label='').values('sample_meta_id', 'tag_label'):
        sample_meta_id = sample.get('sample_meta_id')
        if sample_meta_id and sample_meta_id not in meta_updates:
            meta_updates[sample_meta_id] = sample.get('tag_label')

    if not meta_updates:
        return

    for sample_meta in SampleMeta.objects.filter(id__in=list(meta_updates.keys())).iterator():
        sample_meta.tag_label = meta_updates.get(sample_meta.id)
        sample_meta.save(update_fields=['tag_label'])


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0006_samplemeta_is_nc_sample_samplemeta_tag_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampledata',
            name='tag_label',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.RunPython(forwards_copy_tag_label, backwards_copy_tag_label),
        migrations.RemoveField(
            model_name='samplemeta',
            name='tag_label',
        ),
    ]

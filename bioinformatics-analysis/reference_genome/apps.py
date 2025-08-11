from django.apps import AppConfig


class ReferenceGenomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reference_genome'
    verbose_name = '自建参考基因组'
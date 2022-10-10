from django_filters import filterset

from config.models import Config


class ConfigFilterSet(filterset.FilterSet):
    name = filterset.CharFilter(field_name='name')

    class Meta:
        model = Config
        fields = '__all__'

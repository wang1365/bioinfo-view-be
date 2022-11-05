from django_filters import filterset

from config.models import Config, Resource


class ConfigFilterSet(filterset.FilterSet):
    name = filterset.CharFilter(field_name='name')

    class Meta:
        model = Config
        fields = '__all__'


class ResourceFilterSet(filterset.FilterSet):
    class Meta:
        model = Resource
        fields = {
                  'day': ('exact', 'gt', 'lt', 'gte', 'lte'),
                  }
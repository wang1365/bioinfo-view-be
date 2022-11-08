from django.urls import re_path as url

from . import views

urlpatterns = [
    url(
        r"^/metadata/(?P<taskid>\d+)/(?P<name>[0-9a-zA-Z_]+)/", views.get_meta_data
    ),
    url(
        r"^/data/(?P<taskid>\d+)/(?P<name>[0-9a-zA-Z_]+)/", views.get_raw_data
    ),
]

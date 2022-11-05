from django.urls import re_path as url

from . import views

urlpatterns = [
    url(
        r"^/report/(?P<taskid>\d+)/(?P<name>[a-zA-Z_]+)/metadata", views.get_meta_data
    ),
    url(
        r"^/report/(?P<taskid>\d+)/(?P<name>[a-zA-Z_]+)/data", views.get_raw_data
    ),
]

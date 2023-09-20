from django.urls import re_path as url

from . import views
from report import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'^/report', views.ReportView, basename="samples")

other_urls = [
    url(
        r"^/metadata/(?P<taskid>\d+)/(?P<name>[0-9a-zA-Z_]+)/", views.get_meta_data
    ),
    url(
        r"^/data/(?P<taskid>\d+)/(?P<name>[0-9a-zA-Z_]+)/", views.get_raw_data
    ),
    url(
        r"^/file/", views.read_file
    ),
    url(r'^/pathogen/read',views.pathogen_read)
]

urlpatterns = other_urls + router.urls
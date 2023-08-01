from django.urls import re_path as url

from sample import views
from sample.constants import SAMPLE_META_TEMPLATE_PATH, SAMPLE_TEMPLATE_PATH, SAMPLE_META_TEMPLATE_EN_PATH, SAMPLE_TEMPLATE_EN_PATH
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'^/samples', views.SampleView, basename="samples")

router.register(r'^/sampledatas', views.SampleMetaView, basename="samples_datas")

other_urls = [
    url(r"^/download/(?P<pk>\d+)$", views.download),

    url(
        r"^/samples/template/download",
        lambda req: views.download_by_choices(req, [SAMPLE_TEMPLATE_PATH, SAMPLE_TEMPLATE_EN_PATH]),
    ),

    url(
        r"^/samples/(?P<pk>\d+)/detail",
        views.SampleView.as_view({"get": "retrieve"}),
    ),
    url(
        r"^/samples/query",
        views.SampleView.as_view({"post": "query"}),
    ),
    url(
        r"^/samples/export",
        views.SampleView.as_view({"get": "export"}),
    ),
     url(
        r"^/samplemeta/export",
        views.SampleView.as_view({"get": "export"}),
    ),
    url(r"^/samples/list_fields",
        views.SampleMetaView.as_view({"get": "list_fields"})),

    url(
        r"^/samplemeta/template/download",
        lambda req: views.download_by_choices(req, [SAMPLE_META_TEMPLATE_PATH, SAMPLE_META_TEMPLATE_EN_PATH]),
    ),
    url(r"^/samplemeta/list_fields",
        views.SampleMetaView.as_view({"get": "list_fields"})),

    url(r"^/samplemeta/upload",
        views.SampleUploadView.as_view({"post": "upload_meta"})),

    url(r"^/samples/upload",
        views.SampleUploadView.as_view({"post": "upload"})),
]

urlpatterns = other_urls + router.urls

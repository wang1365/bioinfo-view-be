from django.conf.urls import url

from sample import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'^/samples', views.SampleView, basename="samples")

other_urls = [
    url(r"^/upload", views.SampleUploadView.as_view()),
    url(r"^/download/(?P<pk>\d+)$", views.download),
    url(
        r"^/samples/query",
        views.SampleView.as_view({"post": "query"}),
    ),
    url(
        r"^/samples/export",
        views.SampleView.as_view({"get": "export"}),
    ),
    url(r"^/samples/list_fields",
        views.SampleView.as_view({"get": "list_fields"})),
]

urlpatterns = router.urls + other_urls

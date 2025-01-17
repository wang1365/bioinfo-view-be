from django.urls import re_path as url
from rest_framework import routers

from . import views

urlpatterns = [
    # url(r"^$", views.ProjectsAPIView.as_view()),
    url(r"^$", views.ConfigView.as_view({"get": "list", "post": "create"})),
    url(
        r"^/(?P<pk>\d+)$",
        views.ConfigView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
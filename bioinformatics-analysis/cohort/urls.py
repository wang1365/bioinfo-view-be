from django.urls import re_path as url
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CohortViewSet

router = DefaultRouter()
router.register(r"/", CohortViewSet, basename="cohort")

urlpatterns = [
    url(r"^$", CohortViewSet.as_view({
        "get": "list",
        "post": "create"
    })),
    path("stats_by_task", CohortViewSet.as_view({"get": "stats_by_task"}), name="stats_by_task"),
]


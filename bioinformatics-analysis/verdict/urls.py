from django.urls import re_path as url
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VerdictViewSet

router = DefaultRouter()
router.register(r"/", VerdictViewSet, basename="verdict")

urlpatterns = [
    url(r"^$", VerdictViewSet.as_view({
        "get": "list",
        "post": "create"
    })),
    path("by_patient/", VerdictViewSet.as_view({"get": "by_patient"}), name="diagnosis-by-patient"),
]

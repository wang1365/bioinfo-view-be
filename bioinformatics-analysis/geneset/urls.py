from django.urls import re_path as url
from rest_framework.routers import DefaultRouter

from .views import GenesetViewSet

router = DefaultRouter()
router.register(r"/", GenesetViewSet, basename="geneset")

urlpatterns = [
    url(r"^$", GenesetViewSet.as_view({
        "get": "list",
        "post": "create"
    }))
]

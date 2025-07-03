from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CohortViewSet

router = DefaultRouter()
router.register(r'cohort', CohortViewSet, basename='cohort')

urlpatterns = router.urls


from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'^/patients', views.PatientViewSet, basename="patient")

urlpatterns = router.urls

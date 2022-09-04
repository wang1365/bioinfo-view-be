
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'^/resource_limits', views.ResourceLimitViewSet, basename="resource_limit")

urlpatterns = router.urls

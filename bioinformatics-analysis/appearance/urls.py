
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r"", views.SiteLayoutlViewSet, "site_layout")

urlpatterns = router.urls

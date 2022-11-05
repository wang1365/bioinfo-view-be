from django.urls import re_path as url
from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'^/resources', views.ResourceView, basename="resource")
urlpatterns = router.urls
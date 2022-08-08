from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^site_layout", views.SiteLayoutlViewSet.as_view(), name="site_layout"),
]
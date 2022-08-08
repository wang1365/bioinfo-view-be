from django.conf.urls import url
from rest_framework import routers

from flow import views

router = routers.DefaultRouter()

router.register(r'^/flows', views.FlowView, basename="flows")

other_urls = [
    url(
        r"^/flows/query", views.FlowView.as_view({
            "post": "query"
        })
    ),
    url(
        r"^/flows/list_fields", views.FlowView.as_view({
            "get": "list_types"
        })
    ),
    url(
        r"^/members", views.FlowView.as_view({
            "post": "add_members",
            "delete": "remove_members",
        })
    ),
    url(
        r"^/samples", views.FlowView.as_view({
            "get": "list_samples",
        })
    ),
]


urlpatterns = router.urls + other_urls

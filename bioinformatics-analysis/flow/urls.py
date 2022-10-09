from django.urls import re_path as url
from rest_framework import routers

from flow import views

router = routers.DefaultRouter()
router.register(r'^/flows', views.FlowView, basename="flows")

group_router = routers.DefaultRouter()
group_router.register(r'^/panelGroups', views.PanelGroupView, basename="panelGroups")

panel_router = routers.DefaultRouter()
panel_router.register(r'^/panels', views.PanelView, basename="panels")

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

urlpatterns = group_router.urls + panel_router.urls + router.urls + other_urls

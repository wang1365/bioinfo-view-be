from django.urls import re_path as url
from model_query.views import post_query

urlpatterns = [
    url(r"^/(?P<model_name>.+)$", post_query),
]

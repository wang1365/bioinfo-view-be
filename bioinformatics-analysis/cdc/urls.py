from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^/collect_information$', views.collect_information, name='collect_information'),
]
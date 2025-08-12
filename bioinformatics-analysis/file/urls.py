from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^/database/read$', views.read_file_from_database, name='read_file_from_database'),
    url(r'^/read$', views.read_file, name='read_file'),
]
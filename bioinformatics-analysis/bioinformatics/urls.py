"""bioinformatics-be URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path as url
from django.contrib import admin
from django.urls import include

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^account/", include(("account.urls", "account"),
                              namespace="account")),
    url(r"^project", include(("project.urls", "account"),
                             namespace="project")),
    url(r"^role", include(("rbac.urls", "role"), namespace="role")),
    url(r"^flow", include(("flow.urls", "flow"), namespace="flow")),
    url(r"^sample", include(("sample.urls", "sample"), namespace="sample")),
    url(r"^task", include(("task.urls", "task"), namespace="task")),
    url(r"^config", include(("config.urls", "config"), namespace="config")),
    url(r"^resource", include(("config.resource_urls", "config"), namespace="resource")),
    url(r"^site_config/",
        include(("appearance.urls", "appearance"), namespace="appearance")),
    url(r"^patient", include(("patient.urls", "patient"),
                             namespace="patient")),
    url(r'^model_query',
        include(('model_query.urls', 'model_query'), 'model_query'))
    # 资源限制和使用放在account model上, 直接使用account的接口
    # url(r"^resource_limit", include(("resource_limit.urls", "resource_limit"), namespace="resource_limit")),
]

from django.urls import re_path as url

from task import views

urlpatterns = [
    # url(r"^$", views.ProjectsAPIView.as_view()),
    url(r"^$", views.TaskView.as_view({"get": "list", "post": "create"})),
    url(
        r"^/(?P<pk>\d+)$",
        views.TaskView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),name="single"
    ),
    url("/download/(?P<pk>\d+)$", views.download, name="task_download"),
    url("/run_qc$", views.RunQcView.as_view(), name="run_qc"),
    url("/summary$", views.task_summary, name="task_summary"),
]

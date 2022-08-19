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
import subprocess
import os

from apscheduler.scheduler import Scheduler
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include

from task.models import Task
from config.models import Config
from utils.memory import SystemMemory

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^account/", include(("account.urls", "account"), namespace="account")),
    url(r"^project", include(("project.urls", "account"), namespace="project")),
    url(r"^role", include(("rbac.urls", "role"), namespace="role")),
    url(r"^flow", include(("flow.urls", "flow"), namespace="flow")),
    url(r"^sample", include(("sample.urls", "sample"), namespace="sample")),
    url(r"^task", include(("task.urls", "task"), namespace="task")),
    url(r"^config", include(("config.urls", "config"), namespace="config")),
    url(r"^site_config/", include(("appearance.urls", "appearance"), namespace="appearance")),
    url(r"^patient", include(("patient.urls", "patient"), namespace="patient")),
]


sched = Scheduler()


@sched.interval_schedule(seconds=30)
def run_task():
    max_task = Config.objects.filter(name="max_task").first().value
    max_task = int(max_task) if max_task else 10
    print(f"Hello Scheduler!Start run task, max_task: {max_task}")
    memory_rate = Config.objects.filter(name="memory_rate").first().value
    memory_rate = memory_rate if memory_rate < 1.0 else 1
    running_tasks = Task.objects.filter(status=2).all()
    used_memory = sum(task.memory for task in running_tasks)
    totol_memory = SystemMemory().totol_memory
    running_tasks_count = len(running_tasks)
    if running_tasks_count < max_task and used_memory < totol_memory * memory_rate:
        # run task
        beto_run_tasks = Task.objects.filter(status=1).order_by("-priority", "create_time")[
            0: max_task - running_tasks_count
        ]
        for beto_run_task in beto_run_tasks:
            if used_memory + beto_run_task.memory < totol_memory * memory_rate:
                shell_location = beto_run_task.flow.location
                s = subprocess.Popen(
                    f"/bin/sh -c {shell_location}", env=beto_run_task.env, shell=True
                )
                beto_run_task.status = 2
                beto_run_task.pid = s.pid
                beto_run_task.save()
                used_memory += beto_run_task.memory

@sched.interval_schedule(seconds=3600 * 24 * 30)
def clear_task():
    print("Hello Scheduler!Start clean task disk")
    beto_clean_tasks = Task.objects.filter(status=3, has_cleaned=False).order_by("create_time").all()
    for beto_clean_task in beto_clean_tasks:
        out_dir = beto_clean_task.env.get("OUT_DIR")
        if out_dir:
            subprocess.Popen(f"rm -rf {out_dir}", shell=True)
            beto_clean_task.has_cleaned = True
            beto_clean_task.save()

@sched.interval_schedule(seconds=3600 * 24 * 30)
def clean_task_log():
    print("Hello Scheduler!Start clean task_data dir")
    base = os.path.join(os.path.dirname(settings.BASE_DIR), "task_data")
    os.makedirs(base, exist_ok=True)
    subprocess.Popen(f"rm -rf {base}/*", shell=True)

# sched.start()

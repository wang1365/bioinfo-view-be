"""
WSGI config for bioinformatics-be project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import json
import asyncio
import logging
from functools import wraps

from asgiref.sync import sync_to_async
from django.core.handlers.exception import response_for_exception
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

logger = logging.getLogger('django.request')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bioinformatics.settings.prod")

application = get_wsgi_application()


def convert(get_response):
    if asyncio.iscoroutinefunction(get_response):

        @wraps(get_response)
        async def inner(request):
            try:
                response = await get_response(request)
            except Exception as exc:
                response = await sync_to_async(response_for_exception,
                                               thread_sensitive=False)(request,
                                                                       exc)
            return response

        return inner
    else:

        @wraps(get_response)
        def inner(request):
            try:
                response = get_response(request)

                if response.status_code >= 400:
                    response = HttpResponse(status=200,
                                            content=json.dumps({
                                                'code':
                                                1,
                                                'status_code':
                                                response.status_code,
                                                'data':
                                                str(response.content.decode()),
                                                'msg':
                                                response.reason_phrase
                                            }),
                                            content_type='application/json')
            except Exception as exc:
                response = response_for_exception(request, exc)
            return response

        return inner

application._middleware_chain = convert(application._middleware_chain)
from apscheduler.schedulers.background import BackgroundScheduler
import time

scheduler = BackgroundScheduler()

import logging

# logger = logging.getLogger('job')
# logging.basicConfig(level=logging.INFO,
#                     format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt = '%Y-%m-%d %H:%M:%S',
#                     filename = '/tmp/mylog.txt',
#                     filemode = 'a+')
# 定时任务，打印当前的时间
@scheduler.scheduled_job(trigger='interval', seconds=10, id='test')
def test_job():
    with open("/bioinformatics-analysis/task_data/test2.txt", "w") as f:
        f.write("zzzzzz")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

from apscheduler.schedulers.background import BackgroundScheduler
import time
from django.conf import settings
from django.urls import re_path as url
from django.contrib import admin
from django.urls import include

from task.models import Task
from config.models import Config
from utils.memory import SystemMemory
from flow.core import G_CLIENT

scheduler = BackgroundScheduler()
@scheduler.scheduled_job(trigger='interval', seconds=30, id='run_task')
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
        beto_run_tasks = Task.objects.filter(status=1).order_by(
            "-priority", "create_time")[0:max_task - running_tasks_count]
        for beto_run_task in beto_run_tasks:
            if used_memory + beto_run_task.memory < totol_memory * memory_rate:
                # shell_location = beto_run_task.flow.location
                # s = subprocess.Popen(f"/bin/sh -c {shell_location}",
                #                      env=beto_run_task.env,
                #                      shell=True)
                container = G_CLIENT.containers.run(
                    image=beto_run_task.flow.image_name,
                    environment=beto_run_task.env,
                    volumes={
                        os.getenv("TASK_RESULT_DIR"): {
                            'bind': os.getenv("TASK_DIR"),
                            'mode': 'rw'}},
                    detach=True,
                    network_mode="host"
                )
                beto_run_task.status = 2
                beto_run_task.pid = container.id
                beto_run_task.save()
                used_memory += beto_run_task.memory

scheduler._logger=logger
scheduler.start()

# sched = Scheduler()
#
# import subprocess
# import os
#
# from apscheduler.scheduler import Scheduler
# from django.conf import settings
# from django.urls import re_path as url
# from django.contrib import admin
# from django.urls import include
#
# from task.models import Task
# from config.models import Config
# from utils.memory import SystemMemory
# from flow.core import G_CLIENT
#
# @sched.interval_schedule(seconds=30)
# def run_task():
#     with open("/bioinformatics-analysis/task_data/test.txt", "w") as f:
#         f.write("xxxx")
#     max_task = Config.objects.filter(name="max_task").first().value
#     max_task = int(max_task) if max_task else 10
#     print(f"Hello Scheduler!Start run task, max_task: {max_task}")
#     memory_rate = Config.objects.filter(name="memory_rate").first().value
#     memory_rate = memory_rate if memory_rate < 1.0 else 1
#     running_tasks = Task.objects.filter(status=2).all()
#     used_memory = sum(task.memory for task in running_tasks)
#     totol_memory = SystemMemory().totol_memory
#     running_tasks_count = len(running_tasks)
#     if running_tasks_count < max_task and used_memory < totol_memory * memory_rate:
#         # run task
#         beto_run_tasks = Task.objects.filter(status=1).order_by(
#             "-priority", "create_time")[0:max_task - running_tasks_count]
#         for beto_run_task in beto_run_tasks:
#             if used_memory + beto_run_task.memory < totol_memory * memory_rate:
#                 # shell_location = beto_run_task.flow.location
#                 # s = subprocess.Popen(f"/bin/sh -c {shell_location}",
#                 #                      env=beto_run_task.env,
#                 #                      shell=True)
#                 container = G_CLIENT.containers.run(
#                     image=beto_run_task.flow.image_name,
#                     environment=beto_run_task.env,
#                     volumes={
#                         os.getenv("TASK_RESULT_DIR"): {
#                             'bind': os.getenv("TASK_DIR"),
#                             'mode': 'rw'}},
#                     detach=True,
#                     network_mode="host"
#                 )
#                 beto_run_task.status = 2
#                 beto_run_task.pid = container.id
#                 beto_run_task.save()
#                 used_memory += beto_run_task.memory
#
#
# @sched.interval_schedule(seconds=3600 * 24 * 30)
# def clear_task():
#     print("Hello Scheduler!Start clean task disk")
#     beto_clean_tasks = Task.objects.filter(
#         status=3, has_cleaned=False).order_by("create_time").all()
#     for beto_clean_task in beto_clean_tasks:
#         out_dir = beto_clean_task.env.get("OUT_DIR")
#         if out_dir:
#             subprocess.Popen(f"rm -rf {out_dir}", shell=True)
#             beto_clean_task.has_cleaned = True
#             beto_clean_task.save()
#
#
#
# sched.start()
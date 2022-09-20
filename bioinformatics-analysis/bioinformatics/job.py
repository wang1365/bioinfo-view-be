
import os
from flow.core import G_CLIENT
from utils.memory import SystemMemory
from config.models import Config
from task.models import Task

from utils.hostip import get_host_ip
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess


scheduler = BackgroundScheduler()


# @scheduler.scheduled_job(trigger='interval', seconds=1000, id='test_image')
# def test_image():
#     with open("/bioinformatics-analysis/task_data/test.txt", "w") as f:
#         container = G_CLIENT.containers.run(
#             image="test",
#             environment={
#                 "a": 1,
#                 "result": os.getenv("TASK_RESULT_DIR"),
#                 "ip": get_host_ip()},
#             volumes={
#                 os.getenv("TASK_RESULT_DIR"): {
#                     'bind': os.getenv("TASK_RESULT_DIR"),
#                     'mode': 'rw'}},
#             detach=True,
#             network_mode="host")
#         f.write(container.id)


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
                container = G_CLIENT.containers.run(
                    image=beto_run_task.flow.image_name,
                    environment=beto_run_task.env,
                    volumes={
                        os.getenv("TASK_RESULT_DIR"): {
                            'bind': os.getenv("TASK_RESULT_DIR"),
                            'mode': 'rw'
                        },
                        os.getenv("BIO_ROOT"): {
                            'bind': os.getenv("BIO_ROOT"),
                            'mode': 'rw'
                        },
                    },
                    detach=True,
                    remove=True,
                    network_mode="host"
                )
                beto_run_task.status = 2
                beto_run_task.pid = container.id
                beto_run_task.save()
                used_memory += beto_run_task.memory


@scheduler.scheduled_job(trigger='interval',
                         seconds=3600 * 24 * 30,
                         id='clear_task')
def clear_task():
    print("Hello Scheduler!Start clean task disk")
    beto_clean_tasks = Task.objects.filter(
        status=3, has_cleaned=False).order_by("create_time").all()
    for beto_clean_task in beto_clean_tasks:
        out_dir = beto_clean_task.env.get("OUT_DIR")
        if out_dir:
            subprocess.Popen(f"rm -rf {out_dir}", shell=True)
            beto_clean_task.has_cleaned = True
            beto_clean_task.save()


@scheduler.scheduled_job(trigger='interval',
                         seconds=3600 * 24 * 30,
                         id='clear_task')
def clean_task_log():
    from django.conf import settings
    print("Hello Scheduler!Start clean task_data dir")
    base = os.path.join(os.path.dirname(settings.BASE_DIR), "task_data")
    os.makedirs(base, exist_ok=True)
    subprocess.Popen(f"rm -rf {base}/*", shell=True)


scheduler.start()
import logging
import os

from apscheduler.triggers.interval import IntervalTrigger
from django.core.cache import cache
from django.utils.timezone import now

from flow.core import G_CLIENT
from utils.memory import SystemMemory
from config.models import Config
from task.models import Task

from django.db import close_old_connections
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
    close_old_connections()
    # from django import db
    # for conn in db.connections.all():
    #     conn.close_if_unusable_or_obsolete()

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
                        os.getenv("SAMPLE_DIR"): {
                            'bind': os.getenv("SAMPLE_DIR"),
                            'mode': 'rw'
                        },
                        os.getenv("DATA_DIR"): {
                            'bind': os.getenv("DATA_DIR"),
                            'mode': 'rw'
                        },
                        os.getenv("DATABASE_DIR"): {
                            'bind': os.getenv("DATABASE_DIR"),
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


@scheduler.scheduled_job("cron", day_of_week='*', hour='1', minute='0', second='0')
def cal_disk_config():
    from config.models import Config
    from utils.disk import dir_size
    result_dir = os.getenv("TASK_RESULT_DIR")
    Config.objects.filter(name="disk").update(used=dir_size(result_dir))


@scheduler.scheduled_job("cron", day_of_week='*', hour='23', minute='59', second='0')
def cal_day_disk():
    from task.models import Task
    from datetime import datetime, date
    from utils.disk import dir_size
    from config.models import Resource
    now = datetime.now()
    begin = now.replace(hour=0, minute=0, second=0)
    end = now.replace(hour=23, minute=59, second=59)
    tasks = Task.objects.filter(create_time__gte=begin, create_time__lte=end)
    day_used_disk = 0
    for task in tasks:
        day_used_disk += dir_size(task.env.get("OUT_DIR"))
    Resource.objects.create(typ="disk", value=day_used_disk, day=date.today(), name="task")

@scheduler.scheduled_job("cron", day_of_week='*', hour='0', minute='10', second='0')
def update_running_days():
    key, value = f'job_lock', os.getpid()
    if not cache.add(key, value, 30):
        logging.getLogger().warning(f'Job已被{cache.get(key)}加锁, 忽略执行')
        return
    else:
        logging.getLogger().warning(f'Job加锁 {key} - {value}')
    logging.getLogger('job').info("==========> update_running_days +1")

    # Config.objects.create(name="allowed_running_days", value=365, used=0, create_time=now(), update_time=now())
    if not Config.objects.filter(name="allowed_running_days").exists():
        Config.objects.create(name="allowed_running_days", value=365, used=0, create_time=now(), update_time=now())
        logging.getLogger('job').info("==========> 配置项不存在，新建配置项")

    config = Config.objects.filter(name="allowed_running_days").get()
    config.used += 1
    config.save()


scheduler.start()

from sched import scheduler

from apscheduler.schedulers.background import BackgroundScheduler
from django.db import close_old_connections
from loguru import logger

from flow.core import G_CLIENT
from reference_genome.models import ReferenceGenome

scheduler = BackgroundScheduler()


#

@scheduler.scheduled_job(trigger='interval', seconds=60, id='check_ref_genome_task')
def check_ref_genome_task():
    close_old_connections()
    try:
        # 获取所有status为"todo"的任务
        tasks = ReferenceGenome.objects.filter(status="RUNNING")
        for task in tasks:
            if task.container_id:
                # 检查容器是否存在，如果不存在，设置状态为已完成DONE
                # 说明：使用G_CLIENT检查容器状态, 如果容器不存在，则更新任务状态为DONE
                try:
                    container_status = G_CLIENT.containers.get(task.container_id).status
                except Exception as e:
                    logger.info(f"Container {task.container_name} {task.container_id} not found: {e}")
                    task.status = "DONE"
                    task.save()
                else:
                    logger.info(f"Container {task.container_name} {task.container_id} status: {container_status}")
    finally:
        close_old_connections()



def start_ref_genome_scheduler():
    scheduler.start()

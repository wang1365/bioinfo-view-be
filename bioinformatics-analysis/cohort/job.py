from sched import scheduler

from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpRequest

from task.models import Task
from task.views import read_mut_standard_file_by_name

scheduler = BackgroundScheduler()
# 每隔1分钟执行一次，执行步骤如下：
# 1. 查询task中cohort_status为"todo"的任务
# 2. 对每个任务执行以下操作：
#    - 调用read_mut_standard_file, 其中request中name参数为Mut_WES，获取mut_standard_file，如果不存在则跳过。执行完成后将cohort_status更新为"done"
#    - 解析mut_standard_file这个csv，第一行是header，提取下面这些header： Gene.refGene GeneDetail.refGene AAChange Chr Start End Ref Alt，
#  保存到cohort表中

@scheduler.scheduled_job(trigger='interval', seconds=60, id='check_multi_create_task')
def check_multi_create_task():
    # 获取所有cohort_status为"todo"的任务
    tasks = Task.objects.filter(cohort_status="todo")
    for task in tasks:
        from task.views import read_mut_standard_file
        ret = read_mut_standard_file_by_name("Mut_WES", task.pk)
        mut_standard_file, ok = ret[0], ret[2] == 0
        if mut_standard_file is not None and len(mut_standard_file) > 0:
            task.cohort_status = "done"
            task.save()
            # 解析mut_standard_file，第一行是header，提取下面这些header： Gene.refGene GeneDetail.refGene AAChange Chr Start End Ref Alt，
            header = mut_standard_file[0].split(",")
            task.cohort.update_cohort_info(select=header)
        if ok:
            print(f"Task {task.pk} cohort_status updated to done.")
            task.cohort_status = "done"
            task.save()



def start_cohort_scheduler():
    scheduler.start()


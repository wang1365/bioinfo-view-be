import datetime
from sched import scheduler

from apscheduler.schedulers.background import BackgroundScheduler

from cohort.models import Cohort
from task.models import Task
from task.views import read_mut_standard_file_by_name
from loguru import logger as log

scheduler = BackgroundScheduler()


# 每隔1分钟执行一次，执行步骤如下：
# 1. 查询task中cohort_status为"todo"的任务
# 2. 对每个任务执行以下操作：
#    - 调用read_mut_standard_file, 其中request中name参数为Mut_WES，获取mut_standard_file，如果不存在则跳过。执行完成后将cohort_status更新为"done"
#    - 解析mut_standard_file这个csv，第一行是header，提取下面这些header： Gene.refGene GeneDetail.refGene AAChange Chr Start End Ref Alt，
#  保存到cohort表中

def parse_file_to_cohorts(csv_data, task_id, user_id, panel_id):
    # 解析CSV数据
    lines = csv_data.split('\n')
    headers = lines[0].split('\t')
    header_indexes = [headers.index('Gene.refGene'), headers.index('GeneDetail.refGene'), headers.index('AAChange'),
                      headers.index('Chr'), headers.index('Start'), headers.index('End'), headers.index('Ref'),
                      headers.index('Alt')]
    cohorts = []
    for line in lines[1:]:
        values = line.split('\t')
        if len(values) < len(header_indexes):
            continue
        cohort = Cohort(
            gene_info='|'.join([values[i] for i in header_indexes]),
            panel_id=panel_id,
            task_id=task_id,
            user_id=user_id,
            del_flag=0
        )
        cohorts.append(cohort)
    # 批量插入cohorts
    ret = Cohort.objects.bulk_create(cohorts)
    log.info(f"Insert {len(ret)} cohorts for task {task_id}, user_id {user_id}, panel_id {panel_id}")


@scheduler.scheduled_job(trigger='interval', seconds=180, id='check_cohort')
def check_cohort():
    del_flag = int(datetime.datetime.now().timestamp())
    # 获取所有cohort_status为"todo"的任务
    tasks = Task.objects.filter(cohort_status="todo")
    for task in tasks:
        Cohort.objects.filter(task_id=task.id).update(del_flag=del_flag)

        user_id, task_id, panel_id = task.creator_id, task.id, task.flow.panel_id
        ret = read_mut_standard_file_by_name("Mut_WES", task.pk)
        mut_standard_file, ok = ret[0], ret[2] == 0
        if mut_standard_file is not None and len(mut_standard_file) > 0:
            # 解析mut_standard_file，第一行是header，提取下面这些header： Gene.refGene GeneDetail.refGene AAChange Chr Start End Ref Alt，
            parse_file_to_cohorts(mut_standard_file, task_id, user_id, panel_id)

        log.info(f"Task {task.pk} cohort_status updated to done.")
        task.cohort_status = "done"
        task.save()

    # 将del_flag设置为当前时间戳：仅针对那些task_id在Task表中不存在的cohort记录
    Cohort.objects.exclude(task_id__in=Task.objects.values_list('id', flat=True)).update(del_flag=del_flag)


def start_cohort_scheduler():
    scheduler.start()

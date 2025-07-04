from datetime import datetime

from django.db import connection
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response

from common.viewsets.viewsets import CustomeViewSets
from task.models import Task
from utils.response import response_body
from .models import Cohort

class CohortViewSet(CustomeViewSets):
    queryset = Cohort.objects.filter(del_flag=0)

    def create(self, request, *args, **kwargs):
        # 批量新增
        data = request.data
        if not isinstance(data, list):
            data = [data]

        objs = []
        for item in data:
            objs.append(Cohort(
                ref_gene=item.get('ref_gene', ''),
                chr=item.get('chr', ''),
                start=item.get('start', ''),
                end=item.get('end', ''),
                ref=item.get('ref', ''),
                alt=item.get('alt', ''),
                count=item.get('count', 0),
                panel=item.get('panel', ''),
                task_id=item.get('task_id'),
                user_id=item['user_id'],
            ))

        Cohort.objects.bulk_create(objs)
        return response_body(data=True, msg="success")

    def destroy(self, request, *args, **kwargs):
        # 批量删除
        ids = request.data.get('ids', [])
        if not ids:
            return Response(response_body(code=1, msg="请选择要删除的记录"))

        Cohort.objects.filter(id__in=ids).update(
            del_flag=int(datetime.now().timestamp())
        )
        return response_body(data=True, msg="success")

    @action(detail=False, methods=["get"])
    def stats_by_task(self, request):
        # 根据task_id统计比例
        task_id = request.query_params.get('task_id')
        # 根据task_id查询task对象
        task = Task.objects.get(id=task_id)
        panel_id = task.flow.panel_id
        task_count = Task.objects.filter(flow__panel_id=panel_id).count()
        if not task_id:
            return Response(response_body(code=1, msg="task_id不能为空"))

        # 获取当前task的统计
        with connection.cursor() as cursor:
            cursor.execute(f'''
            select gene_info, count(1) cnt from cohort where panel_id={panel_id} and del_flag = 0 group by gene_info;
            ''')
            result = [{ 'gene_info': row[0], 'cnt': row[1], 'total': task_count } for row in cursor.fetchall()]
        return response_body(data=result, msg="success")

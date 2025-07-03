from datetime import datetime
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response

from common.viewsets.viewsets import CustomeViewSets
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
        if not task_id:
            return Response(response_body(code=1, msg="task_id不能为空"))

        # 获取当前task的统计
        current_task_stats = Cohort.objects.filter(
            task_id=task_id,
            del_flag=0
        ).values(
            'ref_gene', 'chr', 'start', 'end', 'ref', 'alt'
        ).annotate(
            task_count=Sum('count')
        )

        # 获取所有相同panel的统计
        panel = request.query_params.get('panel')
        if not panel:
            return Response(response_body(code=1, msg="panel不能为空"))

        all_panel_stats = Cohort.objects.filter(
            panel=panel,
            del_flag=0
        ).values(
            'ref_gene', 'chr', 'start', 'end', 'ref', 'alt'
        ).annotate(
            total_count=Sum('count')
        )

        # 合并结果
        result = []
        for item in current_task_stats:
            ref_gene = item['ref_gene']
            chr = item['chr']
            start = item['start']
            end = item['end']
            ref = item['ref']
            alt = item['alt']

            # 查找相同panel的总数
            total = next((x for x in all_panel_stats
                         if x['ref_gene'] == ref_gene
                         and x['chr'] == chr
                         and x['start'] == start
                         and x['end'] == end
                         and x['ref'] == ref
                         and x['alt'] == alt), None)

            if total:
                ratio = item['task_count'] / total['total_count'] if total['total_count'] else 0
                result.append({
                    'ref_gene': ref_gene,
                    'chr': chr,
                    'start': start,
                    'end': end,
                    'ref': ref,
                    'alt': alt,
                    'task_count': item['task_count'],
                    'total_count': total['total_count'],
                    'ratio': ratio
                })

        return response_body(data=result, msg="success")

#!/usr/bin/env python3
import json
from common.filters import CommonFilters

from flow.models import FlowMembers


class FlowFilters(CommonFilters):
    SEARCH_FIELDS = [
        'flow_category', 'name', 'desp', 'location', 'alignment_tool'
    ]


class FilterByAccount:

    def filter_queryset(self, request, queryset, view):
        account_id = request.account.id

        # 超级管理员不进行过滤
        if "super" in request.role_list:
            return queryset

        if "admin" in request.role_list:
            payload = request.parser_context['request'].body
            if not payload:
                return queryset
            body = json.loads(payload)
            if 'account_id' not in body:
                return queryset
            account_id = body['account_id']

        flow_ids = FlowMembers.objects.filter(
            account_id=account_id).values_list('flow_id')
        queryset = queryset.filter(id__in=flow_ids)
        return queryset

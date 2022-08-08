#!/usr/bin/env python3

import json

from django.db.models import Q


class CommonFilters:
    SEARCH_FIELDS = []

    def filter_queryset(self, request, queryset, view):
        queryset = queryset.order_by('create_time')

        filter_info = self.extract_filters(request.parser_context['request'])
        search_keyword = filter_info['search_keyword']
        payload = filter_info['payload']

        queryset = self.filter_queryset_by_search(queryset, search_keyword)
        queryset = self.filter_queryset_by_filters(queryset, payload)

        return queryset

    def extract_filters(self, context):
        request = context.parser_context['request']

        keyword = ""
        payload = {}

        if request.method == 'GET':
            keyword = request.GET.get('s', '')

        elif request.method == 'POST':
            body = json.loads(request.body)
            payload = body.get('filters', {})
            keyword = body.get('search_keyword')

        return {
            "search_keyword": keyword,
            "payload": payload,
        }

    def filter_queryset_by_search(self, queryset, keyword):
        if not keyword or len(keyword) <= 0:
            return queryset

        q = Q()
        for f in self.SEARCH_FIELDS:
            q = q | Q(**{'{}__icontains'.format(f): keyword})

        return queryset.filter(q)

    def filter_queryset_by_filters(self, queryset, params):
        q = Q()

        for filter_param in params:
            condition = self._transform_filter_param(filter_param)

            if not condition:
                continue

            q = q & condition

        return queryset.filter(q)

    def _operator_actions(self):
        return {
            'in': lambda k, v: Q(**{'{}__in'.format(k): v}),
            'ni': lambda k, v: ~Q(**{'{}__in'.format(k): v}),
            'eq': lambda k, v: Q(**{'{}'.format(k): v}),
            'ne': lambda k, v: ~Q(**{'{}'.format(k): v}),
            'gt': lambda k, v: Q(**{'{}__gt'.format(k): v}),
            'gte': lambda k, v: Q(**{'{}__gte'.format(k): v}),
            'lt': lambda k, v: Q(**{'{}__lt'.format(k): v}),
            'lte': lambda k, v: Q(**{'{}__lte'.format(k): v}),
            'between': lambda k, v: Q(**{
                '{}__gte'.format(k): v[0],
                '{}__lte'.format(k): v[1],
            }),
        }

    def _transform_filter_param(self, filter_param):
        operator_actions = self._operator_actions()
        operator = filter_param['op']

        action = operator_actions.get(operator, None)
        if action is None:
            return {}

        return action(filter_param['key'], filter_param['values'])

#!/usr/bin/env python3
import json
from common.filters import CommonFilters
from django.db.models import Q

from account import constants as account_constant
from project.utils import get_sampleids_by_projectids, get_user_by_project_ids


class SampleUserFilter:

    def filter_queryset(self, request, queryset, view):
        projects = {}

        if request.method == 'POST':
            body = json.loads(request.parser_context['request'].body)
            projects = body.get('project_id', {})
        include = projects.get('in', [])
        if include:
            return queryset

        if account_constant.NORMAL in request.role_list:
            queryset = queryset.filter(user=request.account)
        elif account_constant.ADMIN in request.role_list:
            queryset = queryset.filter(
                Q(user__user2role__role__code=account_constant.NORMAL) | Q(user=request.account))

        return queryset


class SampleProjectFilters:

    def filter_queryset(self, request, queryset, view):
        projects = {}

        if request.method == 'POST':
            body = json.loads(request.parser_context['request'].body)
            projects = body.get('project_id', {})

        include = projects.get('in', [])
        exclude = projects.get('not_in', [])

        include_sample_ids = get_sampleids_by_projectids(include)
        exclude_sample_ids = get_sampleids_by_projectids(exclude)

        if include:
            queryset = queryset.filter(id__in=include_sample_ids)

        if exclude:
            queryset = queryset.exclude(id__in=exclude_sample_ids)

        return queryset


class SampleKeywordFilters:
    def filter_queryset(self, request, queryset, view):
        if request.method != 'POST':
            return queryset

        body = json.loads(request.parser_context['request'].body)
        keyword = body.get('keyword', '')
        if not keyword:
            return queryset

        return queryset.filter(sample_meta__patient__name__icontains=keyword)


class SampleFilters(CommonFilters):
    SEARCH_FIELDS = ['company', 'index_type']


class SampleMetaFilters(CommonFilters):
    SEARCH_FIELDS = []

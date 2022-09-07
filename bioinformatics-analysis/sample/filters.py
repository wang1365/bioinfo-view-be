#!/usr/bin/env python3
import json
from common.filters import CommonFilters

from project.utils import get_sampleids_by_projectids, get_user_by_project_ids


class SampleUserFilter:

    def filter_queryset(self, request, queryset, view):
        projects = {}
        if "admin" in request.role_list:
            return queryset

        if request.method == 'POST':
            body = json.loads(request.parser_context['request'].body)
            projects = body.get('project_id', {})

        include = projects.get('in', [])

        if include:
            return queryset

        return queryset.filter(user_id__in=[0, request.account.id])


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


class SampleFilters(CommonFilters):
    SEARCH_FIELDS = ['company', 'index_type']


class SampleMetaFilters(CommonFilters):
    SEARCH_FIELDS = []

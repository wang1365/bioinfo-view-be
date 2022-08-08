#!/usr/bin/env python3

from project.models import Project, ProjectMembers


def get_sampleids_by_projectids(project_ids):
    projects = Project.objects.filter(id__in=project_ids)
    sample_ids = set()

    for project in projects:
        sample_ids |= {s.id for s in project.samples.all()}

    return sample_ids


def get_user_by_project_ids(project_ids):
    return ProjectMembers.objects.filter(
        project_id__in=project_ids).values_list('account_id', flat=True
    )

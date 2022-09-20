# Create your views here.
import re
import subprocess
from rest_framework.viewsets import ModelViewSet

from account.models import Account
from project.models import Project, ProjectMembers
from project.serializer import ProjectSerializer
from sample.models import Sample
from task.models import Task
from utils.paginator import PageNumberPagination
from utils.response import response_body


class ProjectsAPIView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data["total_task_count"] = Task.objects.filter(
            project=instance).count()
        response_data["pending_task_count"] = Task.objects.filter(
            project=instance, status=1).count()
        response_data["running_task_count"] = Task.objects.filter(
            project=instance, status=2).count()
        response_data["finished_task_count"] = Task.objects.filter(
            project=instance, status=3).count()
        response_data["failured_task_count"] = Task.objects.filter(
            project=instance, status=4).count()
        response_data["canceled_task_count"] = Task.objects.filter(
            project=instance, status=5).count()
        return response_body(data=response_data)

    def _code_exists(self, code):
        if Project.objects.filter(code=code).exists():
            return True
        return False

    def create(self, request, *args, **kwargs):
        # project_name = request.data.get("name", "")
        # if Project.objects.filter(owner=request.account, name=project_name).exists():
        #     return response_body(code=1, msg=f"您已创建了名为{project_name}的项目")
        samples = [
            Sample.objects.get(
                pk=i) for i in request.data.get(
                "samples", [])]
        members = [request.account]
        members.extend([Account.objects.get(pk=i)
                        for i in request.data.get("members", [])])
        # code = request.data.get("code", "")
        # if self._code_exists(code):
        #     return response_body(code=1, msg=f"已存在项目编码{code}的项目")
        parent = request.data.get("parent", None)
        try:
            project = Project.objects.create(
                **{
                    "owner": request.account,
                    "name": request.data.get("name", ""),
                    "desc": request.data.get("desc", ""),
                    "parent_id": parent
                    # "code": request.data.get("code", ""),
                }
            )
        except Exception as e:
            return response_body(code=1, msg=e.args[0])
        if samples:
            project.samples.set(samples)
        if members:
            members_list = [
                ProjectMembers(
                    account=member,
                    project=project) for member in set(members)]
            ProjectMembers.objects.bulk_create(objs=members_list)
        bs = self.serializer_class(project, many=False)
        return response_body(data=bs.data)

    def list(self, request, *args, **kwargs):
        query_name = request.GET.get("name")
        query_parent = request.GET.get("parent_id")
        if "admin" in request.role_list:
            projects = Project.objects.filter(is_visible=True)
        else:
            projects = Project.objects.filter(
                members__id__in=[
                    request.account.id],
                is_visible=True)
        if query_name:
            projects = projects.filter(name__contains=query_name)
        if query_parent:
            projects = projects.filter(parent_id=int(query_parent))
        elif not request.GET.get("all_level", ""):
            projects = projects.filter(parent__isnull=True)
        else:
            pass
        projects = projects.order_by("-create_time")
        page = self.paginate_queryset(projects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return response_body(
                data={"results": serializer.data, "count": len(projects)}
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_builtin:
            return response_body(code=1, msg="内置项目不能删除")
        if request.account.id == instance.owner.id or (
                "admin" in request.role_list):
            tasks = Task.objects.filter(project=instance).all()
            for task in tasks:
                out_dir = task.env.get("OUT_DIR")
                if out_dir:
                    subprocess.Popen(f"rm -rf {out_dir}", shell=True)
                task.delete()
            Project.objects.filter(pk=instance.id).delete()
            return response_body(data=True)
        return response_body(code=1, msg="非项目创建者不能删除项目", data=False)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.account.id == instance.owner.id or (
                "admin" in request.role_list):
            samples = [
                Sample.objects.get(
                    pk=i) for i in set(
                    request.data.get(
                        "samples",
                        []))]
            members = [
                Account.objects.get(
                    pk=i) for i in request.data.get(
                    "members", [])]
            instance.samples.set(samples)
            if members:
                instance.members.clear()
                members_list = [
                    ProjectMembers(
                        account=member,
                        project=instance) for member in members]
                ProjectMembers.objects.bulk_create(objs=members_list)
            if request.data.get("name"):
                instance.name = request.data.get("name")
            if request.data.get("desc"):
                instance.name = request.data.get("desc")
            # code = request.data.get("code", "")
            # if code:
            #     if self._code_exists(code):
            #         return response_body(code=1, msg=f"已存在项目编码{code}的项目")
            #     elif not code.isalnum() or re.findall('[\u4e00-\u9fa5]', code):
            #         return response_body(code=1, msg=f"项目编码只能由大小写英文字母组成")
            #     else:
            #         instance.code = code
            instance.save()
            bs = self.serializer_class(instance, many=False)
            return response_body(data=bs.data)
        return response_body(code=1, msg="非项目创建者或管理员不能修改项目", data=False)

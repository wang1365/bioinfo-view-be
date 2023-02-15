import logging
from datetime import timedelta
from django.db.models import Sum

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.decorators import action
from rest_framework.viewsets import mixins, GenericViewSet
from django_filters import rest_framework as filters
from django.db.models import Count
from django.db.models.functions import TruncMonth

from account.auth import authenticate, create_access_token
from account.forms import LoginForm, RegisterForm
from account.models import Account
from account.serializer import AccountSerializer
from rbac.models import Role, User2Role
from utils.paginator import PageNumberPagination
from utils.response import response_body
from utils.site import get_md5
from account import constants as account_constant
from task.models import Task
from config.models import Config

logger = logging.getLogger(__name__)


class UserFilter(filters.FilterSet):
    keyword = filters.CharFilter(method='filter_keyword', help_text='搜索关键字')

    class Meta:
        model = Account
        fields = ('keyword',)

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(Q(username__icontains=value)
                               | Q(nickname__icontains=value)
                               | Q(email__icontains=value))


class UsersAPIView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet):
    # 序列化类
    serializer_class = AccountSerializer
    # 查询集和结果集
    queryset = Account.objects.all()
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    filter_class = UserFilter

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        ret = self.serializer_class(request.account).data
        ret["role_list"] = request.role_list
        return response_body(data=ret)

    def get_pk(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return self.kwargs.get(lookup_url_kwarg)

    @action(detail=True, methods=['put'])
    def reset_password(self, request, *args, **kwargs):
        user = Account.objects.filter(pk=request.user_id).first()
        user.password = get_md5(request.data.get("password"))
        user.save()
        return response_body(data="重置密码成功")

    def update(self, request, *args, **kwargs):
        sum_dict = Account.objects.all().aggregate(sum_disk=Sum('disk_limit'))
        disk_limit = request.data.get("disk_limit")
        if disk_limit:
            disk_config = Config.objects.filter(name="disk").first()
            sum_disk = sum_dict.get("sum_disk", 0)
            if sum_disk + int(disk_limit) > disk_config.value:
                return response_body(status_code=200, code=1, msg=f"您最多只剩下{disk_config.value-sum_disk}MB的空间可配置")
        resp = super().update(request, *args, **kwargs)
        return response_body(
            data=resp.data
        )

    @action(detail=True, methods=['patch'])
    def change_password(self, request, *args, **kwargs):
        user = Account.objects.filter(pk=request.user_id).first()
        if user.password != get_md5(request.data.get("old_password")):
            return response_body(code=1, msg="原密码不正确")
        user.password = get_md5(request.data.get("new_password"))
        user.save()
        return response_body(data="密码修改成功")

    def list(self, request, *args, **kwargs):
        # 获取所有数据
        if account_constant.ADMIN in request.role_list:
            # accounts = Account.objects.filter(
            #     Q(is_delete=False) & (Q(user2role__role__code=account_constant.NORMAL) | Q(pk=request.account.id))).all()
            accounts = Account.objects.filter(
                Q(is_delete=False) & (
                            Q(parent=request.account) | Q(pk=request.account.id))).all()
        elif account_constant.SUPER in request.role_list:
            accounts = Account.objects.filter(
                is_delete=False, user2role__role__code__in=[
                    account_constant.SUPER, account_constant.ADMIN]).all()
        else:
            accounts = Account.objects.filter(is_delete=False)

        # 支持关键字检索
        keyword = request.query_params.get('keyword')
        if keyword:
            accounts = accounts.filter(Q(username__icontains=keyword)
                                       | Q(nickname__icontains=keyword)
                                       | Q(email__icontains=keyword))
        pg = PageNumberPagination()
        # 在数据库中获取分页的数据,
        pager_accounts = pg.paginate_queryset(
            queryset=accounts, request=request, view=self
        )
        # 对数据进行序列化
        ser = AccountSerializer(instance=pager_accounts, many=True)
        item_list = ser.data
        for item in item_list:
            item["role"] = list(
                User2Role.objects.filter(
                    user=item["id"]).values_list(
                    "role__code",
                    flat=True))
            item['running_task'] = Task.objects.filter(creator_id=item["id"], status=2).count()
        return response_body(
            data={"item_list": item_list, "total_count": accounts.count()}
        )

    @action(detail=False, methods=["post"])
    def create_user(self, request, *args, **kwargs):
        register_form = RegisterForm(request.data, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data["username"]
            nickname = register_form.cleaned_data["nickname"]
            email = register_form.cleaned_data["email"]
            password = get_md5(register_form.cleaned_data["password"])

            try:
                account = Account(
                    username=username,
                    nickname=nickname,
                    email=email,
                    password=password,
                    is_active=True,
                    parent=request.account
                )
                account.save()
            except Exception as e:
                return response_body(code=400, msg=str(e), status_code=400)
            if "super" in request.role_list:
                role = Role.objects.filter(code="admin").first()
            elif "admin" in request.role_list:
                role = Role.objects.filter(code="normal").first()
            User2Role.objects.create(user=account, role=role)
            return response_body(data=AccountSerializer(account).data)
        else:
            email_error = register_form.errors.get("email")
            pwd_error = register_form.errors.get("password_again")
            username_error = register_form.errors.get("username")
            error = register_form.errors.get_json_data()
            if pwd_error:
                error = pwd_error[0]
            if email_error:
                error = email_error[0]
            if username_error:
                error = username_error[0]
            return response_body(msg=error, code=400, status_code=400)

    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        obj_form = LoginForm(request.data)
        if obj_form.is_valid():
            username = obj_form.cleaned_data.get("username", None)
            password = obj_form.cleaned_data.get("password", None)
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                user.save()
                access_token_expires = timedelta(
                    minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                )
                return response_body(
                    data={
                        "access_token": create_access_token(
                            data={"user_id": user.id},
                            expires_delta=access_token_expires,
                        ),
                        "token_type": "bearer",
                    }
                )
            else:
                return response_body(code=401, msg="用户名或密码错误", status_code=401)
        else:
            return response_body(
                code=400, msg=obj_form.errors.get_json_data(), status_code=400)

    @action(detail=False, methods=["delete"])
    def delete_user(self, request, *args, **kwargs):
        # count = Account.objects.filter(
        #     pk__in=request.data.get(
        #         "ids", [])).update(
        #     is_delete=1)
        count = Account.objects.filter(
            pk__in=request.data.get(
                "ids", [])).delete()
        User2Role.objects.filter(
            user_id__in=request.data.get(
                "ids", [])).delete()
        return response_body(data=count)

    @action(detail=False, methods=["post"])
    def manager(self, request, *args, **kwargs):
        role = request.data.get("role", [])
        if role:
            User2Role.objects.filter(
                user_id=request.data.get('userid')).delete()
            for code in role:
                role = Role.objects.filter(code=code).first()
                User2Role.objects.create(
                    user_id=request.data.get('userid'), role=role)
        is_active = request.data.get("is_active")
        department = request.data.get("department")
        reset = request.data.get("reset")
        if is_active is not None:
            Account.objects.filter(
                id=request.data.get('userid')).update(
                is_active=is_active)
        if department is not None:
            Account.objects.filter(
                id=request.data.get('userid')).update(
                department=department)
        if reset:
            Account.objects.filter(
                id=request.data.get('userid')).update(
                password=get_md5("123456"))
        return response_body(data=True)

    @action(detail=False, methods=["get"])
    def summary(self, request, *args, **kwargs):
        if account_constant.ADMIN in request.role_list:
            accounts = Account.objects.filter(
                is_delete=False, user2role__role__code__in=[
                    account_constant.NORMAL, account_constant.ADMIN]).all()
        elif account_constant.SUPER in request.role_list:
            accounts = Account.objects.filter(
                is_delete=False, user2role__role__code__in=[
                    account_constant.SUPER, account_constant.ADMIN]).all()
        else:
            accounts = Account.objects.filter(is_delete=False)
        data = accounts.annotate(month=TruncMonth('create_time')).values('month').annotate(count=Count('id'))
        return response_body(
            data=[item for item in data]
        )


def account_validate(request):
    type = request.GET.get("type")
    id = request.GET.get("id")
    user = get_object_or_404(Account, id=id)
    logger.info(type)
    if user.is_active:
        return HttpResponseRedirect("/")

    c_sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))
    sign = request.GET.get("sign")
    if sign != c_sign:
        return HttpResponseForbidden()
    user.is_active = True
    user.save()
    # return HttpResponse("邮箱验证成功")
    return render(request, "account/result.html")

import logging
from datetime import timedelta
import re

from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseRedirect
# from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.views import APIView

from account.auth import authenticate, create_access_token
from account.constants import ADMIN, POST_ACTION_LOGIN, POST_ACTION_REGISTER
from account.forms import LoginForm, RegisterForm
# from rest_framework.response import Response
from account.models import Account
from account.serializer import AccountSerializer
from rbac.models import Role, User2Role
from utils.hostip import get_host_ip
from utils.message import send_email
from utils.paginator import PageNumberPagination
from utils.response import response_body
from utils.site import get_current_site, get_md5

logger = logging.getLogger(__name__)


class UsersAPIView(ListCreateAPIView):
    # 序列化类
    serializer_class = AccountSerializer
    # 查询集和结果集
    queryset = Account.objects.all()
    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get(self, request, *args, **kwargs):
        userser = self.serializer_class(request.account)
        ret = userser.data
        ret["role_list"] = request.role_list
        return response_body(data=ret)

    def patch(self, request, *args, **kwargs):
        user = Account.objects.filter(pk=request.user_id).first()
        data = request.data.copy()
        if "name" in data:
            name = data["name"]
            if not name.isalpha() or re.findall('[\u4e00-\u9fa5]', name):
                return response_body(msg='用户名只能由大小写英文字母组成', code=1)
        if "password" in data:
            data["password"] = get_md5(data["password"])
        if "email" not in data:
            data["email"] = user.email
        bs = self.serializer_class(user, data=data, context={"request": request})
        if bs.is_valid():
            bs.save()
            return response_body(data="更新成功")
        else:
            return response_body(msg=bs.errors, code=1)

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")
        # 若参数为register则为注册，创建用户
        if action == POST_ACTION_REGISTER:
            return self.create(request, *args, **kwargs)
        elif action == POST_ACTION_LOGIN:
            obj_form = LoginForm(request.data)
            if obj_form.is_valid():
                email = obj_form.cleaned_data.get("email", None)
                password = obj_form.cleaned_data.get("password", None)
                user = authenticate(email=email, password=password)
                if user and user.is_active:
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
                elif user and not user.is_active:
                    return response_body(code=1, msg="邮箱未验证, 请前往邮箱验证或找管理员激活")
                else:
                    return response_body(code=1, msg="邮箱或密码错误")
            else:
                return response_body(code=1, msg=obj_form.errors.get_json_data())


    # 创建用户
    # 重写的CreateModelMixin中的方法：用于用户的创建
    def create(self, request, *args, **kwargs):
        register_form = RegisterForm(request.data, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data["username"]
            email = register_form.cleaned_data["email"]
            password = get_md5(register_form.cleaned_data["password"])
            # 创建用户
            account = Account(username=username, email=email, password=password)
            account.save()
            if "super" in request.role_list:
                role = Role.objects.filter(code="admin").first()
            elif "admin" in request.role_list:
                role = Role.objects.filter(code="normal").first()
            User2Role.objects.create(user=account, role=role)
            site = get_current_site().domain
            sign = get_md5(get_md5(settings.SECRET_KEY + str(account.id)))
            if settings.DEBUG:
                site = f"{get_host_ip()}:8000"
            path = reverse("account:result")
            url = "http://{site}{path}?type=validation&id={id}&sign={sign}".format(
                site=site, path=path, id=account.id, sign=sign
            )

            content = """
                                        <p>请点击下面链接验证您的邮箱</p>

                                        <a href="{url}" rel="bookmark">{url}</a>

                                        再次感谢您！
                                        <br />
                                        如果上面链接无法打开，请将此链接复制至浏览器。
                                        {url}
                                        """.format(
                url=url
            )
            send_email(subject="验证您的电子邮箱", to_addr=account.email, content=content)
            return response_body(data="验证邮件已发送, 请前往邮箱认证")
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
            return response_body(msg=error, code=1)


class UserManagerView(APIView):

    def get(self, request, *args, **kwargs):
        # 获取所有数据
        accounts = Account.objects.filter(is_delete=False).all()
        # 创建分页对象
        pg = PageNumberPagination()
        # 在数据库中获取分页的数据,
        pager_accounts = pg.paginate_queryset(
            queryset=accounts, request=request, view=self
        )
        # 对数据进行序列化
        ser = AccountSerializer(instance=pager_accounts, many=True)
        item_list = ser.data
        for item in item_list:
            item["role"] = list(User2Role.objects.filter(user=item["id"]).values_list("role__code", flat=True))
        return response_body(
            data={"item_list": item_list, "total_count": len(accounts)}
        )

    def patch(self, request, *args, **kwargs):
        if ADMIN in request.role_list:
            role = request.data.get("role", [])
            if role:
                User2Role.objects.filter(user_id=request.data.get('userid')).delete()
                for code in role:
                    role = Role.objects.filter(code=code).first()
                    User2Role.objects.create(user_id=request.data.get('userid'), role=role)
            is_active = request.data.get("is_active")
            department = request.data.get("department")
            reset = request.data.get("reset")
            if is_active is not None:
                Account.objects.filter(id=request.data.get('userid')).update(is_active=is_active)
            if department is not None:
                Account.objects.filter(id=request.data.get('userid')).update(department=department)
            if reset:
                Account.objects.filter(id=request.data.get('userid')).update(password=get_md5("123456"))
            return response_body(data=True)
        return response_body(code=1, msg="非管理员用户不能修改用户角色")

    def delete(self, request, *args, **kwargs):
        if ADMIN in request.role_list:
            count = Account.objects.filter(pk__in=request.data.get("ids", [])).update(
                is_delete=1
            )
            User2Role.objects.filter(user_id__in=request.data.get("ids", [])).delete()
            return response_body(data=count)
        return response_body(code=1, msg="非管理员用户不能删除用户")


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

import jwt
from django.conf import settings
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from jwt import PyJWTError

from account.models import Account
from config.models import Config
from rbac.models import User2Role, Role
from utils.response import response_body
import os, sys

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.is_english = request.META.get("HTTP_LANGUAGE", "") in ("en-US", "en")

        if 'AUTH_DISABLED' in os.environ:
            return
        token = request.META.get("HTTP_AUTHORIZATION") or request.COOKIES.get("token")
        if not token:
            if (
                    request.path.startswith("/account")
                    and request.method == "POST"
                    or request.path == reverse("account:result")
            ) or (request.path.startswith("/task") and request.method.lower() == "put") \
                    or (request.path.startswith("/site_config") and request.method.lower() == 'get'):
                pass
            else:
                return response_body(code=1, msg="未登录", status_code=401)
        else:
            try:
                payload = jwt.decode(
                    token.encode("utf8"), settings.SECRET_KEY, algorithms=[ALGORITHM]
                )
                request.user_id = payload["user_id"]
                user = Account.objects.get(id=request.user_id)
                request.account = user if user else ""
                roles = User2Role.objects.filter(user=user).values("role__code")
                if len(roles) == 0:
                    print("security user: ", user.username, " role is empty")
                    role = Role.objects.filter(code="admin").first()
                    User2Role.objects.create(user=user, role=role)
                roles = User2Role.objects.filter(user=user).values("role__code")
                request.role_list = [role.get('role__code') for role in roles]

                if not self.check_license_expired(user):
                    if request.is_english:
                        return response_body(code=1, msg="The system usage time has expired！", status_code=401)
                    return response_body(code=1, msg="系统使用期限已到！", status_code=401)
            except PyJWTError:
                return response_body(code=1, msg="token已失效", status_code=401)

    def check_license_expired(self, user):
        if user.username == 'super':
            return True

        config = Config.objects.get(name="allowed_running_days")
        return config.value >= config.used

import jwt
from django.conf import settings
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from jwt import PyJWTError

from account.models import Account
from rbac.models import User2Role
from utils.response import response_body

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get("HTTP_AUTHORIZATION") or request.COOKIES.get("token")
        if not token:
            if (
                request.path.startswith("/account")
                and request.method == "POST"
                or request.path == reverse("account:result")
            ) or (request.path.startswith("/task") and request.method.lower() == "put"):
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
                request.role_list = [role.get('role__code') for role in roles]

            except PyJWTError:
                return response_body(code=1, msg="token已失效", status_code=401)

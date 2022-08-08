from datetime import datetime, timedelta

import jwt
from django.conf import settings
from jwt import PyJWTError

from account.models import Account
from utils.site import get_md5

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def authenticate(email, password):
    return Account.objects.filter(
        email=email, password=get_md5(password), is_delete=False
    ).first()


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt.decode("utf8")


def login_required(func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION") or request.COOKIES["token"]
        try:
            payload = jwt.decode(
                token.encode("utf8"), settings.SECRET_KEY, algorithms=[ALGORITHM]
            )
        except PyJWTError:
            raise Exception("用户token验证没有通过")
        user = Account.objects.get(id=payload["user_id"])
        if not user:
            raise Exception("系统用户不存在")
        return func(request, *args, **kwargs)

    return wrapper

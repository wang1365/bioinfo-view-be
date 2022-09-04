import json
from typing import Any

from django.http import HttpResponse

from utils.json_encoder import JsonToDatetime


class Response:

    def __init__(self, data="", errors="", code=200):
        self.data = data
        self.errors = errors
        self.code = code


def response_body(
    status_code: int = 200,
    code: int = 0,
    msg: str = "",
    data: Any = "",
):
    return HttpResponse(
        status=status_code,
        content=json.dumps(
            {
                "code": code,
                "msg": msg,
                "data": data,
                'status_code': status_code
            },
            ensure_ascii=False,
            cls=JsonToDatetime),
    )

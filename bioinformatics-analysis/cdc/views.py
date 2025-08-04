import json
import os
from django.http import JsonResponse
from rest_framework.decorators import api_view
from utils.response import response_body
from utils.env import database_dir

@api_view(['POST'])
def collect_information(request):
    """
    根据body中的参数，调用本地脚本后生成数据返回
        {
        "virusName": [],
        # 病毒分型
        "virusTypes": [],
        # 宿主
        "host": [],
        # 宿主基因组版本
        "hostGenomeVersion": [],
        # 自定义数据库名称
        "customDatabaseName": [],
    }
    """
    # 从请求body中获取json
    json_data = request.body.decode('utf-8')
    # 解析json
    json_data = json.loads(json_data)


    return response_body(
        status_code=200,
        code=0,
        msg='',
        data=[]
    )

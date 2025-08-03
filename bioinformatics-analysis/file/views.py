import os
from django.http import JsonResponse
from rest_framework.decorators import api_view
from utils.response import response_body
from utils.env import database_dir

@api_view(['GET'])
def read_file_from_database(request):
    """
    读取本地文件内容
    GET /file/read?path=文件路径
    """
    file_path = os.path.join(database_dir, request.GET.get('path'))

    if not file_path:
        return response_body(
            data=None,
            status_code=400,
            code=-1,
            msg='缺少path参数'
        )
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return response_body(
            data=None,
            status_code=404,
            code=-1,
            msg=f'文件不存在: {file_path}'
        )
    
    # 检查是否为文件（不是目录）
    if not os.path.isfile(file_path):
        return response_body(
            data=None,
            status_code=400,
            code=-1,
            msg=f'路径不是文件: {file_path}'
        )
    
    try:
        # 尝试以UTF-8编码读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return response_body(data=content)
    except UnicodeDecodeError:
        try:
            # 如果UTF-8失败，尝试GBK编码
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
            return response_body(data=content)
        except Exception as e:
            return response_body(
                data=None,
                status_code=500,
                code=-1,
                msg=f'文件编码错误，无法读取: {str(e)}'
            )
    except Exception as e:
        return response_body(
            data=None,
            status_code=500,
            code=-1,
            msg=f'读取文件失败: {str(e)}'
        )
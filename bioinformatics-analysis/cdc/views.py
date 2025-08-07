import json
import os
from django.http import JsonResponse
from loguru import logger
from rest_framework.decorators import api_view
from utils.response import response_body
from utils.env import database_dir
from utils.env import database_dir


@api_view(['POST'])
def collect_information(request):
    """
    根据body中的参数，调用本地脚本后生成数据返回
        {
        "virusName": [],
        # 病毒分型
        "virusType": [],
        # 宿主
        "host": [],
        # 宿主基因组版本
        "hostGenomeVersion": [],
        # 自定义数据库名称
        "customDatabase": [],
    }
    """
    # 从请求body中获取json
    json_data = request.body.decode('utf-8')
    # 解析json
    json_data = json.loads(json_data)

    # 拼接参数，脚本参数说明如下：
    # sh make.ref.sh /data/bioinfo/database_dir/Pathogen_database/customize_ref_db/   /data/bioinfo/database_dir/Pathogen_database/ref_seq_db/   human   hg19   Norovirus   ALL   hg19_Norovirus    F
    #
    # 脚本：sh make.ref.sh
    # 参数说明：
    # 1. /data/bioinfo/database_dir/Pathogen_database/customize_ref_db/
    # 2. /data/bioinfo/database_dir/Pathogen_database/ref_seq_db/
    # 3. host:          human  多个值的话用逗号分割
    # 4. host_pick:     hg19   多个值的话用逗号分割
    # 5. sp:            Norovirus  多个值的话用逗号分割
    # 6. sp_pick:       ALL        多个值的话用逗号分割
    # 7. new_ref_name:  hg19_Norovirus
    # 8. F

    customize_ref_db = os.path.join(database_dir, "Pathogen_database/customize_ref_db/")
    ref_seq_db = os.path.join(database_dir, "Pathogen_database/ref/")
    sp, sp_pick = ','.join(json_data['virusName']), ','.join(json_data['virusType'])
    host, host_pick = json_data['host'], json_data['hostGenomeVersion']
    new_ref_name = json_data['customDatabase']

    # 最终参数
    params = f"{customize_ref_db} {ref_seq_db} {host} {host_pick} {sp} {sp_pick} {new_ref_name}"
    # 脚本路径
    bash = os.path.join(database_dir, "Pathogen_database/bin/make.ref.sh")
    # 最终命令
    cmd = f"sh {bash} {params}"

    logger.info(f"cmd: {cmd}")

    # 调用本地脚本 /data/bioinfo/database_dir/Pathogen_database/bin/make.ref.sh
    exit_code = os.system(cmd)
    logger.info(f"exit_code: {exit_code}")

    # 脚本执行完成后，会在脚本所在文件夹下生成2个文件，分别是host_mapdb.info 和  sp_mapdb.info
    # 读取这2个文件的内容
    out_dir = os.path.join(database_dir, 'Pathogen_database/customize_ref_db/hg19_Norovirus')
    host_mapdb_info = os.path.join(out_dir, "host_mapdb.info")
    sp_mapdb_info = os.path.join(out_dir, "sp_mapdb.info")
    with open(host_mapdb_info, "r") as f:
        host_mapdb_info = f.read()
    with open(sp_mapdb_info, "r") as f:
        sp_mapdb_info = f.read()


    return response_body(
        status_code=200,
        code=0,
        msg='',
        data={
            "host_mapdb_info": host_mapdb_info,
            "sp_mapdb_info": sp_mapdb_info
        }
    )

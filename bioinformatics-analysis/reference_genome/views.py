import json
import os
from pathlib import Path

from django.db.models import Q
from docker.models.containers import Container
from loguru import logger
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from account import constants as account_constant
from common.filters import CommonFilters
from config.models import Config
from flow.core import G_CLIENT
from utils.env import database_dir, bio_root, task_result_dir, data_dir, sample_dir, all
from utils.paginator import PageNumberPaginationWithWrapper
from utils.response import response_body
from .models import ReferenceGenome
from .serializers import (
    ReferenceGenomeSerializer,
    ReferenceGenomeCreateSerializer,
    ReferenceGenomeListSerializer
)


class ReferenceGenomeFilter(CommonFilters):
    """自建参考基因组过滤器"""

    def filter_queryset(self, request, qs, view):
        # 基础过滤（不包括排序）
        filter_info = self.extract_filters(request.parser_context['request'])
        search_keyword = filter_info['search_keyword']
        payload = filter_info['payload']

        qs = self.filter_queryset_by_search(qs, search_keyword)
        qs = self.filter_queryset_by_filters(qs, payload)

        # 只显示未删除的记录
        qs = qs.filter(is_deleted=False)

        # 根据自定义数据库名搜索
        custom_database = request.GET.get('custom_database')
        if custom_database:
            qs = qs.filter(custom_database__icontains=custom_database)

        # 根据宿主搜索
        host = request.GET.get('host')
        if host:
            qs = qs.filter(host__icontains=host)

        # 根据宿主基因组版本搜索
        host_genome_version = request.GET.get('host_genome_version')
        if host_genome_version:
            qs = qs.filter(host_genome_version__icontains=host_genome_version)

        # 覆盖基类的create_time排序，改为按id倒序
        qs = qs.order_by('-id')

        return qs


class ReferenceGenomeViewSet(ModelViewSet):
    """自建参考基因组视图集"""

    queryset = ReferenceGenome.objects.all()
    serializer_class = ReferenceGenomeSerializer
    pagination_class = PageNumberPaginationWithWrapper
    filter_backends = [ReferenceGenomeFilter]

    def get_serializer_class(self):
        """根据不同的action返回不同的序列化器"""
        if self.action == 'create':
            return ReferenceGenomeCreateSerializer
        elif self.action == 'list':
            return ReferenceGenomeListSerializer
        return ReferenceGenomeSerializer

    def get_queryset(self):
        """获取查询集，只返回未删除的记录"""
        return ReferenceGenome.objects.filter(is_deleted=False).order_by('-id')

    def list(self, request, *args, **kwargs):
        """查询参考基因组列表"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """新建参考基因组"""
        data = request.data.copy()
        data["creator"] = request.account.id

        # 处理host_map_db和sp_map_db文件写入
        custom_database = data.get('custom_database')
        host_map_db = data.get('host_map_db')
        sp_map_db = data.get('sp_map_db')

        # 创建目录
        db_dir = Path(database_dir) / f'Pathogen_database/customize_ref_db/{custom_database}'
        db_dir.mkdir(parents=True, exist_ok=True)

        # 处理host_map_db数据（如果是字符串直接使用，如果是JSON则转换为字符串）
        host_content = host_map_db if isinstance(host_map_db, str) else json.dumps(host_map_db, ensure_ascii=False,
                                                                                   indent=2)

        # 写入host_map_db文件
        host_file_path = db_dir / 'host_mapdb.info'
        with open(host_file_path, 'w', encoding='utf-8') as f:
            f.write(host_content)
        data['host_seq_file'] = str(host_file_path)

        # 处理sp_map_db数据（如果是字符串直接使用，如果是JSON则转换为字符串）
        sp_content = sp_map_db if isinstance(sp_map_db, str) else json.dumps(sp_map_db, ensure_ascii=False, indent=2)

        # 写入sp_map_db文件
        virus_file_path = db_dir / 'sp_mapdb.info'
        with open(virus_file_path, 'w', encoding='utf-8') as f:
            f.write(sp_content)
        data['virus_seq_file'] = str(virus_file_path)

        virus_name = data.get('virus_name')
        virus_type = data.get('virus_type')
        host = data.get('host')
        host_pick = data.get('host_genome_version')
        host, host_pick = host or '-', host_pick or '-'

        result, container_name, container_id = run_docker(
            host= host,
            host_pick=host_pick,
            sp=virus_name,
            sp_pick=virus_type,
            new_ref_name= custom_database,
            index='T'
        )

        data['message'] = result
        data['container_name'] = container_name
        data['container_id'] = container_id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(f"Created database files for {custom_database}: {host_file_path}, {virus_file_path}")


        # 返回完整的对象信息
        instance = serializer.instance
        response_serializer = ReferenceGenomeSerializer(instance)
        return response_body(data=response_serializer.data, msg=f"创建成功: {result}")

    def retrieve(self, request, *args, **kwargs):
        """查询参考基因组详情"""
        instance = self.get_object()

        # 权限检查：普通用户只能查看自己创建的
        if (account_constant.NORMAL in request.role_list and
                instance.creator != request.account):
            return response_body(code=403, msg="无权限访问此资源")

        serializer = self.get_serializer(instance)
        return response_body(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新参考基因组"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 权限检查：只有创建者可以修改
        if instance.creator != request.account:
            return response_body(code=403, msg="无权限修改此资源")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return response_body(data=serializer.data, msg="更新成功")

    def destroy(self, request, *args, **kwargs):
        """删除参考基因组（软删除）"""
        instance = self.get_object()

        # 执行软删除
        instance.soft_delete()
        return response_body(data={}, msg="删除成功")

    @action(methods=['post'], detail=True)
    def restore(self, request, pk=None):
        """恢复已删除的参考基因组"""
        try:
            instance = ReferenceGenome.objects.get(pk=pk, is_deleted=True)
        except ReferenceGenome.DoesNotExist:
            return response_body(code=404, msg="资源不存在或未被删除")

        # 权限检查：只有创建者可以恢复
        if instance.creator != request.account:
            return response_body(code=403, msg="无权限恢复此资源")

        instance.is_deleted = False
        instance.save()

        serializer = self.get_serializer(instance)
        return response_body(data=serializer.data, msg="恢复成功")

    @action(methods=['get'], detail=False)
    def statistics(self, request):
        """获取参考基因组统计信息"""
        queryset = self.get_queryset()

        # 权限控制
        if account_constant.NORMAL in request.role_list:
            queryset = queryset.filter(creator=request.account)
        elif account_constant.ADMIN in request.role_list:
            queryset = queryset.filter(
                Q(creator__user2role__role__code=account_constant.NORMAL)
                | Q(creator=request.account)
            )

        total_count = queryset.count()
        host_stats = queryset.values('host').distinct().count()

        data = {
            'total_count': total_count,
            'unique_hosts': host_stats,
        }

        return response_body(data=data)

def run_docker(new_ref_name, host, host_pick, sp, sp_pick, index='F'):
    params ={
        'HOST': host or '-',
        'HOSTPICK': host_pick or '-',
        'SP': ','.join(sp or []),
        'SPPICK': ','.join(sp_pick or []),
        'NEWREFNAME': new_ref_name,
        'INDEX': index,
    }

    config = Config.objects.filter(name="ref_genome_docker_image")[0]
    image = config.data or ''

    environment = all.copy() | params
    _ = lambda x: {'bind': x, 'mode': 'rw'}
    volumes = {
        task_result_dir: _(task_result_dir),
        bio_root: _(bio_root),
        sample_dir: _(sample_dir),
        data_dir: _(data_dir),
        database_dir: _(database_dir),
        "/etc/localtime": _("/etc/localtime")
    }
    logger.info(f"Start Run docker image: {image} {environment} {volumes}")

    container_name, container_id = '', ''
    try:
        container: Container = G_CLIENT.containers.run(
            image=image,
            environment=environment,
            volumes=volumes,
            detach=True,
            remove=True,
            network_mode="host"
        )
        container_name, container_id = container.name, container.id
        logger.info(f"启动容器: {container.name} (ID: {container.id})")
        if index == 'F':
            container.wait()
    except Exception as e:
        logger.error(f"Run docker image error: {e}")
        return str(e), container_name, container_id
    else:
        logs = f"Run docker image: {image}"
        logger.info(logs)
        return logs, container_name, container_id



@api_view(['GET'])
def check_file(request):
    """
    检查文件是否存在
    """
    custom_database = request.GET.get('custom_database')
    out_dir = str(Path(database_dir) / f'Pathogen_database/customize_ref_db/{custom_database}')
    if not os.path.exists(out_dir) or not os.path.exists(out_dir):
        return response_body(
            status_code=200,
            code=0,
            msg=f'',
            data={
                "ok": False,
                "msg": f"文件不存在: {out_dir}",
            }
        )

    host_mapdb_info = str(Path(out_dir) / "host_mapdb.info")
    sp_mapdb_info = str(Path(out_dir) / "sp_mapdb.info")
    if not os.path.exists(host_mapdb_info) or not os.path.exists(sp_mapdb_info):
        return response_body(
            status_code=200,
            code=0,
            msg=f'文件不存在: {host_mapdb_info}, {sp_mapdb_info}',
            data={
                "ok": False,
                "msg": f"文件不存在: {host_mapdb_info}, {sp_mapdb_info}",
            }
        )
    return response_body(
        status_code=200,
        code=0,
        msg=f'',
        data={
            "ok": True,
            "msg": f"",
        }
    )


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

    virus_name, virus_type = json_data.get('virusName'), json_data.get('virusType')
    host, host_pick = json_data.get('host'), json_data.get('hostGenomeVersion')
    new_ref_name = json_data['customDatabase']

    # 调用本地脚本 /data/bioinfo/database_dir/Pathogen_database/bin/make.ref.sh
    result, _, _ = run_docker(
        host=host,
        host_pick=host_pick,
        sp=virus_name,
        sp_pick=virus_type,
        new_ref_name=new_ref_name,
    )

    # 脚本执行完成后，会在脚本所在文件夹下生成2个文件，分别是host_mapdb.info 和  sp_mapdb.info
    # 读取这2个文件的内容
    out_dir = Path(database_dir) / f'Pathogen_database/customize_ref_db/{new_ref_name}'

    # 读取结果文件
    host_mapdb_info = str(out_dir / "host_mapdb.info")
    sp_mapdb_info = str(out_dir / "sp_mapdb.info")
    if not os.path.exists(host_mapdb_info) or not os.path.exists(sp_mapdb_info):
        return response_body(
            status_code=500,
            code=1,
            msg=f'生成数据库失败，文件不存在: {host_mapdb_info}, {sp_mapdb_info}',
            data={}
        )

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

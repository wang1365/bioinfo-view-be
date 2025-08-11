from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from account import constants as account_constant

from .models import ReferenceGenome
from .serializers import (
    ReferenceGenomeSerializer,
    ReferenceGenomeCreateSerializer,
    ReferenceGenomeListSerializer
)
from utils.response import response_body
from utils.paginator import PageNumberPaginationWithWrapper
from common.filters import CommonFilters


class ReferenceGenomeFilter(CommonFilters):
    """自建参考基因组过滤器"""
    
    def filter_queryset(self, request, qs, view):
        # 基础过滤
        qs = super().filter_queryset(request, qs, view)
        
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
        return ReferenceGenome.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        """查询参考基因组列表"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # 权限控制：普通用户只能看到自己创建的
        if account_constant.NORMAL in request.role_list:
            queryset = queryset.filter(creator=request.account)
        elif account_constant.ADMIN in request.role_list:
            # 管理员可以看到所有普通用户和自己创建的
            queryset = queryset.filter(
                Q(creator__user2role__role__code=account_constant.NORMAL)
                | Q(creator=request.account)
            )

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
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 返回完整的对象信息
        instance = serializer.instance
        response_serializer = ReferenceGenomeSerializer(instance)
        return response_body(data=response_serializer.data, msg="创建成功")

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
        
        request.data['creator'] = request.account.id
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        
        return response_body(data=serializer.data, msg="更新成功")

    def destroy(self, request, *args, **kwargs):
        """删除参考基因组（软删除）"""
        instance = self.get_object()
        
        # 权限检查：只有创建者可以删除
        if instance.creator != request.account:
            return response_body(code=403, msg="无权限删除此资源")
        
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
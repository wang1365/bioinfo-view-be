from django.urls import re_path as url, path
from rest_framework.routers import DefaultRouter
from .views import ReferenceGenomeViewSet

router = DefaultRouter()
router.register(r'reference-genomes', ReferenceGenomeViewSet, basename='reference-genome')

urlpatterns = [
    # 自建参考基因组相关的URL会通过router自动生成
    # GET /reference-genomes/ - 查询参考基因组列表
    # POST /reference-genomes/ - 新建参考基因组
    # GET /reference-genomes/{id}/ - 查询参考基因组详情
    # PUT /reference-genomes/{id}/ - 更新参考基因组
    # PATCH /reference-genomes/{id}/ - 部分更新参考基因组
    # DELETE /reference-genomes/{id}/ - 删除参考基因组（软删除）
    # POST /reference-genomes/{id}/restore/ - 恢复已删除的参考基因组
    # GET /reference-genomes/statistics/ - 获取统计信息
]

urlpatterns += router.urls
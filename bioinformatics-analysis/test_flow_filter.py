
import os
import django
from django.conf import settings

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioinformatics.settings.dev')
django.setup()

from flow.filters import FlowFilters
from flow.models import Flow
from django.test import RequestFactory

def test_flow_filter():
    print("Testing FlowFilters...")
    
    # 检查 SEARCH_FIELDS
    if 'location' in FlowFilters.SEARCH_FIELDS:
        print("FAIL: 'location' is still in FlowFilters.SEARCH_FIELDS")
    else:
        print("PASS: 'location' is removed from FlowFilters.SEARCH_FIELDS")

    # 模拟请求
    factory = RequestFactory()
    request = factory.get('/flow/flows/', {'keyword': 'rp', 'page': 1, 'size': 100})
    
    # 创建过滤器实例
    # 注意：CommonFilters 通常需要 request.query_params 或类似的东西，
    # 具体取决于它的实现。这里我们假设它是一个标准的 DRF 或 Django FilterSet。
    # 让我们看看 CommonFilters 是如何实现的。
    
    # 由于我们修改了代码，只要 SEARCH_FIELDS 中没有 location，理论上就不会构建包含 location 的查询。
    
    # 尝试构建查询
    qs = Flow.objects.all()
    filter_instance = FlowFilters(request.GET, queryset=qs)
    
    try:
        # 尝试获取过滤后的查询集
        filtered_qs = filter_instance.qs
        # 强制执行查询以触发潜在的 SQL 生成错误
        print(f"Filtered query: {filtered_qs.query}")
        print("PASS: Filter query generation successful")
    except Exception as e:
        print(f"FAIL: Filter query generation failed with error: {e}")

if __name__ == "__main__":
    test_flow_filter()

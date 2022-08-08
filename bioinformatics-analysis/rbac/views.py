from rest_framework.viewsets import ModelViewSet

from rbac.models import Role
from rbac.serializer import RoleSerializer
from utils.paginator import PageNumberPagination
from utils.response import response_body

# Create your views here.

class RolesAPIView(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return response_body(data=resp.data.get('results'))

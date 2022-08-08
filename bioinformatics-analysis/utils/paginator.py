from rest_framework.pagination import PageNumberPagination as _PageNumberPagination

from utils.response import response_body


class PageNumberPagination(_PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    # page_size_query_param 相当于临时更改默认的page_size
    page_size_query_param = "size"
    max_page_size = 10000


class PageNumberPaginationWithWrapper(PageNumberPagination):

    def get_paginated_response(self, data):
        return response_body(
            data={
                "count": self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            }
        )

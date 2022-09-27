from django.http import QueryDict

from utils.response import response_body


class CreateModelMixin:
    def create_data(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            return request.data.dict()
        return request.data

    def deal_with_create_error(self, serializer):
        return response_body(code=1, data=serializer.errors, msg="error")

    def create(self, request, *args, **kwargs):
        data = self.create_data(request, *args, **kwargs)

        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=False)

        if not is_valid:
            return self.deal_with_create_error(serializer)

        self.perform_create(serializer)
        return response_body(data=serializer.data, msg="success")

    def perform_create(self, serializer):
        serializer.save()


class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response_body(data=serializer.data, msg="success")


class RetrieveModelMixin:
    def post_retrieve(self, data, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)
        self.post_retrieve(data, request, *args, **kwargs)
        return response_body(data=data, msg="success")

    def serializer_data(self, data, **args):
        return data


class UpdateModelMixin:
    def update_data(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            return request.data.dict()
        return request.data

    def deal_with_update_error(self, serializer):
        return response_body(code=1, data=serializer.errors, msg="error")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = self.update_data(request, *args, **kwargs)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        is_valid = serializer.is_valid(raise_exception=False)

        if not is_valid:
            return self.deal_with_update_error(serializer)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return response_body(data=serializer.data, msg="success")

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response_body(data=instance.id, msg="success")

    def perform_destroy(self, instance):
        instance.delete()

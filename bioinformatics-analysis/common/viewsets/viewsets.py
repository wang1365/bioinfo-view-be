#!/usr/bin/env python3

from rest_framework.viewsets import GenericViewSet

from common.viewsets import mixins


class CustomeViewSets(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    pass

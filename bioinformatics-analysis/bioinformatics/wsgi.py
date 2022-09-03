"""
WSGI config for bioinformatics-be project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bioinformatics.settings.prod")

application = get_wsgi_application()

import json
import asyncio
import logging
import types
from functools import wraps

from asgiref.sync import async_to_sync, sync_to_async

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, MiddlewareNotUsed
from django.core.signals import request_finished
from django.db import connections, transaction
from django.urls import get_resolver, set_urlconf
from django.utils.log import log_response
from django.utils.module_loading import import_string
from django.http import HttpResponse

from django.core.handlers.exception import convert_exception_to_response, response_for_exception

logger = logging.getLogger('django.request')


def convert(get_response):
    """
    Wrap the given get_response callable in exception-to-response conversion.

    All exceptions will be converted. All known 4xx exceptions (Http404,
    PermissionDenied, MultiPartParserError, SuspiciousOperation) will be
    converted to the appropriate response, and all other exceptions will be
    converted to 500 responses.

    This decorator is automatically applied to all middleware to ensure that
    no middleware leaks an exception and that the next middleware in the stack
    can rely on getting a response instead of an exception.
    """
    if asyncio.iscoroutinefunction(get_response):

        @wraps(get_response)
        async def inner(request):
            try:
                response = await get_response(request)
            except Exception as exc:
                response = await sync_to_async(response_for_exception,
                                               thread_sensitive=False)(request,
                                                                       exc)
            return response

        return inner
    else:

        @wraps(get_response)
        def inner(request):
            try:
                response = get_response(request)

                if response.status_code != 200:
                    response = HttpResponse(status=200,
                                            content=json.dumps({
                                                'code':
                                                response.status_code,
                                                'data':
                                                str(response.content.decode()),
                                                'message':
                                                response.reason_phrase
                                            }),
                                            content_type='application/json')
            except Exception as exc:
                response = response_for_exception(request, exc)
            return response

        return inner


application._middleware_chain = convert(application._middleware_chain)

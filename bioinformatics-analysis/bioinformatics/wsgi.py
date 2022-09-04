"""
WSGI config for bioinformatics-be project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import json
import asyncio
import logging
from functools import wraps

from asgiref.sync import sync_to_async
from django.core.handlers.exception import response_for_exception
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

logger = logging.getLogger('django.request')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bioinformatics.settings.prod")

application = get_wsgi_application()


def convert(get_response):
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

                if response.status_code >= 400:
                    response = HttpResponse(status=200,
                                            content=json.dumps({
                                                'code':
                                                1,
                                                'status_code':
                                                response.status_code,
                                                'data':
                                                str(response.content.decode()),
                                                'msg':
                                                response.reason_phrase
                                            }),
                                            content_type='application/json')
            except Exception as exc:
                response = response_for_exception(request, exc)
            return response

        return inner


application._middleware_chain = convert(application._middleware_chain)

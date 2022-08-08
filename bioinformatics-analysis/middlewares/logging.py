import time
import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

logging.basicConfig(level=logging.INFO)

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        request._datetime = datetime.now().strftime("%d/%b/%Y %H:%M:%S")

    def process_response(self, request, response):
        execute_time = time.time() - request.start_time
        path = request.get_full_path()
        logging.info('[%s] %s %s execute_time %f' % (request._datetime, request.method, path, execute_time))
        return response
from .utils.log import log
import json
from django.utils.deprecation import MiddlewareMixin

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ghi log cho request
        if request.path != "/slack/log/" and request.path != "/log/":
          log(f"Request: {request.method} {request.path}")
        try:
          response = self.get_response(request)
        except Exception as e:
          log(f"middleware.py>> Middleware: Error: {e}")
        
        return response
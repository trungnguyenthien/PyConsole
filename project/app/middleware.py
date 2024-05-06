from .utils.log import log
import json
from django.utils.deprecation import MiddlewareMixin

class RequestLoggerMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
      
    def process_exception(self, request, exception):
      log(json.dumps({'request': request, 'exception': exception }))

    def __call__(self, request):
        # Ghi log cho request
        if request.path != "/slack/log/":
          log(f"Request: {request.method} {request.path}")
        
        try:
          response = self.get_response(request)
        except Exception as e:
          log(f"Middleware: Error: {e}")
        
        return response
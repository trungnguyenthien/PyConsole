from .utils.log import log

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
      
    def process_exception(self, request, exception):
      log({'request': request, 'exception': exception })

    def __call__(self, request):
        # Ghi log cho request
        if request.path != "/slack/log/":
          log(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        return response
from .log import log

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ghi log cho request
        log(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        return response
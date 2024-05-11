from django.shortcuts import render
from django.http import HttpResponse
from .utils import log as logger
import json

# ===============> Un-used libraris <===============
# import asyncio

# ===============> Create your views here <===============
def console_log(request):
  # (1) Get all added logs
  logs = logger.all_logs()

  # (2) Chuyển đổi danh sách LogItem thành danh sách các dictionary
  logs_dict = [log.to_dict() for log in logs]

  # (3) Serialize danh sách dictionary thành JSON (logs_json)
  logs_json = json.dumps(logs_dict)

  # (4) Render (logs_json) sử dụng `console.html` template
  return render(request, 'console.html', {'logs_json': logs_json})

def home(request):
  text = f"<h1>THIS HOMEPAGE</h1>"
  return HttpResponse(text)

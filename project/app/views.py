from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from . import log
import json

# Create your views here.
def console(request):
    logs = log.all_logs()
    # Chuyển đổi danh sách LogItem thành danh sách các dictionary
    logs_dict = [log.to_dict() for log in logs]
    # Serialize danh sách dictionary thành JSON
    logs_json = json.dumps(logs_dict)
    # print(logs_json)
    return render(request, 'console.html',  {'logs_json': logs_json})


def home(request):
    text = f"<h1>THIS HOMEPAGE</h1>"
    return HttpResponse(text)
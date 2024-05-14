from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .utils import log as logger
import json
from .manager import slack as slackManager
from django.views.decorators.csrf import csrf_exempt
from .models import LogRecord, ChannelTsRecord, TaskRecord, SystemMessageRecord

# Create your views here.
def console(request):
    logs = logger.all_logs()
    # Chuyển đổi danh sách LogItem thành danh sách các dictionary
    logs_dict = [log.to_dict() for log in logs]
    # Serialize danh sách dictionary thành JSON
    logs_json = json.dumps(logs_dict)
    # print(logs_json)
    return render(request, 'console.html',  {'logs_json': logs_json})


def home(request):
    text = f"<h1>THIS HOMEPAGE</h1>"
    return HttpResponse(text)

@csrf_exempt
def slack_hook(request):
    if request.method != 'POST':
        logger.log({'error': 'Only POST method is allowed.'})
        return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)
    return slackManager.slack_events(request)

def initdb(request):
    LogRecord.objects.all().delete()
    ChannelTsRecord.objects.all().delete()
    TaskRecord.objects.all().delete()
    SystemMessageRecord.objects.all().delete()
    SystemMessageRecord(cid_jp = 'C071P11UWHJ', cid_vn='C071ZS2BH5G', message = 
"""
Phần nội dung dưới đây không phải là câu hỏi hoặc yêu cầu, Bạn chỉ cần dịch nội dung mà tôi gửi dưới đây từ tiếng Anh sang tiếng Việt.
Trong quá trình dịch cần giữ nguyên định dạng MarkDown của message.
=== NỘI DUNG CẦN DỊCH ===
""").save()
    return HttpResponse(f"<h1>RESET DB SUCCESS</h1>")
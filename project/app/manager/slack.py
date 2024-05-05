# views.py
from django.http import HttpResponse
from ..utils.log import log
from django.http import JsonResponse
import json

def slack_events(request):
    # Lấy dữ liệu từ yêu cầu Slack và giải mã từ UTF-8
    body = request.body.decode("utf-8")
    headers = dict(request.headers)

    # Log headers và body với format dễ đọc
    log(json.dumps(headers, indent=2))  # JSON format cho headers
    log(json.dumps(json.loads(body), indent=2))  # JSON format cho body

    json_data = json.loads(body)
    
    # Kiểm tra loại sự kiện
    if 'type' in json_data and json_data['type'] == 'url_verification':
        # Trả lại challenge code mà Slack gửi
        return JsonResponse({'challenge': json_data['challenge']})

    # event_type = json_data['event']['type']
    # Kiểm tra sự kiện "message" và xử lý
    if 'event' in json_data and json_data['event']['type'] == 'message':
        return handle_message_event(json_data)
    else:
        return HttpResponse("NOT YET HANDLE THIS EVENT", status=200)

def handle_message_event(json_data):
    # Trích xuất và log tin nhắn
    channel_id = json_data.get('team_id', '')
    
    try:
        message_text = json_data['event']['message'].get('text', '')
        ts = json_data['event']['message'].get('ts', '')
        is_edited = True
    except:
        ts = json_data['event'].get('ts', '')
        message_text = json_data['event'].get('text', '')
        is_edited = False
    
    log(f"Received message: {message_text} \nts = {ts} \nchannel_id = {channel_id} \nis_edited = {is_edited}")
    return HttpResponse("OK", status=200)

### BOT FUNCTIONS ----------------------------------------------------------------

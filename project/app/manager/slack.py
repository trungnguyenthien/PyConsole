# views.py
from django.http import HttpResponse
from ..utils.log import log
from django.http import JsonResponse
import json
from ..service import slack as slack_service
from ..service import database as database_service
from ..service import chatgpt as chatgpt_service
# import asyncio
# from asgiref.sync import sync_to_async

# async_request_text = sync_to_async(chatgpt_service.request_text, thread_sensitive=False)


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
    channel_id = json_data['event'].get('channel', '')
    if database_service.is_channel_jp(channel_id) == False:
        return HttpResponse("SKIP", status=200)

    try:
        message_text = json_data['event']['message'].get('text', '')
        ts = json_data['event']['message'].get('ts', '')
        is_edited = True
    except:
        ts = json_data['event'].get('ts', '')
        message_text = json_data['event'].get('text', '')
        is_edited = False

    channel_vn = database_service.get_channel_vn(channel_id)
    message_ts_vn = database_service.get_message_ts_vn(channel_id, ts)

    log(
        f"""
Received message: {message_text}
ts = {ts}
channel_id = {channel_id}
is_edited = {is_edited}
channel_vn = {channel_vn}
message_ts_vn = {message_ts_vn}
message_ts_vn_type = {type(message_ts_vn)}
""")

    log(f'=====> Replying... <=====')
    gpt_reply = chatgpt_service.request_text(
        database_service.get_system_rule(channel_id),
        database_service.get_assistant_rule(channel_id),
        message_text
    )
    try:
        log(f'GPT reply 222 = {gpt_reply}')

        if message_ts_vn is None:
            # New Message
            log(f'none-message_ts_vn')
            # log(f'Send <message_ts_vn is None> gpt_reply = {gpt_reply}>')
            # slack_service.send_new_message(channel_vn, gpt_reply)
        else:
            log(f'message_ts_vn')
            # Update Message
            # log(f'Send <message_ts_vn is Available> gpt_reply = {gpt_reply}')
            # slack_service.update_message(channel_vn, ts, gpt_reply)

        log(f'message_ts_vn has beed sent')
        return HttpResponse("OK", status=200)
    except Exception as e:
        log(f"Error occurred: {e}")
        return None  # Return None or handle the error as appropriate for your use case

# BOT FUNCTIONS ----------------------------------------------------------------

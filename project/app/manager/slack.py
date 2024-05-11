# views.py
from django.http import HttpResponse
from ..utils.log import log
from django.http import JsonResponse
import json
import threading
from ..service import slack as slack_service
from ..service import database as database_service
from ..service import chatgpt as chatgpt_service
# import asyncio
# from asgiref.sync import sync_to_async

# async_request_text = sync_to_async(chatgpt_service.request_text, thread_sensitive=False)

repsponse_to_slack_received_event = JsonResponse({'status': 'ok'}, status=200)


def slack_events(request):
    # Lấy dữ liệu từ yêu cầu Slack và giải mã từ UTF-8
    body = request.body.decode("utf-8")
    headers = dict(request.headers)
    log("EVENT HEADER\n" + json.dumps(headers, indent=2))
    log("EVENT POSTBODY\n" + json.dumps(json.loads(body), indent=2))
    json_data = json.loads(body)

    # Kiểm tra loại sự kiện
    if 'type' in json_data and json_data['type'] == 'url_verification':
        # Trả lại challenge code mà Slack gửi
        return JsonResponse({'challenge': json_data['challenge']})

    # Kiểm tra sự kiện "message" và xử lý
    if 'event' in json_data and json_data['event']['type'] == 'message':
        handle_message_event(json_data)

    return repsponse_to_slack_received_event


def handle_message_event(json_data):
    # Trích xuất và log tin nhắn
    channel_id = json_data['event'].get('channel', '')
    log(f'handle_message_event = {channel_id}')
    if database_service.is_channel_jp(channel_id) == False:
        log(f'is_channel_jp = {False}')
        return

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

    log(f"""
Received message: {message_text}
ts = {ts}
channel_id = {channel_id}
is_edited = {is_edited}
channel_vn = {channel_vn}
message_ts_vn = {message_ts_vn}
message_ts_vn_type = {type(message_ts_vn)}
""")
    gpt_reply = chatgpt_service.request_text(
        database_service.get_system_rule(channel_id),
        # database_service.get_assistant_rule(channel_id),
        message_text
    )
    try:
        log(f'gpt_reply = {gpt_reply}')
        if message_ts_vn is None:
            # New Message
            slack_service.send_new_message(channel_vn, gpt_reply)
        else:
            # Update Message
            slack_service.update_message(channel_vn, ts, gpt_reply)
        
        log(f'Message has beed sent to vn_channel')
    except Exception as e:
        log(f"manager/slack.py>> Error occurred: {e}")

# BOT FUNCTIONS ----------------------------------------------------------------

# views.py

from ..utils.log import log
from django.http import JsonResponse
import json
from ..service import slack as slack_service
from ..service import database as database_service
from ..service import chatgpt as chatgpt_service

# ===============> Un-used libraris <===============
# from django.http import HttpResponse
# import threading
# import asyncio
# from asgiref.sync import sync_to_async

# ===============> Init <===============
# async_request_text = sync_to_async(chatgpt_service.request_text, thread_sensitive=False)

repsponse_to_slack_received_event = JsonResponse({'status': 'ok'}, status=200)

# ===============> Export functions <===============
def slack_events(request):
  # (1) Lấy dữ liệu từ yêu cầu Slack và giải mã từ UTF-8
  body = request.body.decode("utf-8")
  headers = dict(request.headers)
  log("EVENT HEADER\n" + json.dumps(headers, indent=2))
  log("EVENT POSTBODY\n" + json.dumps(json.loads(body), indent=2))
  json_data = json.loads(body)

  # (2) Kiểm tra loại sự kiện
  if 'type' in json_data and json_data['type'] == 'url_verification':
    # Trả lại challenge code mà Slack gửi
    response = JsonResponse({'challenge': json_data['challenge']})
  else:
    response = repsponse_to_slack_received_event

  # (3) Kiểm tra sự kiện "message" và xử lý
  if 'event' in json_data and json_data['event']['type'] == 'message':
    _handle_message_event(json_data)

  return response

# ===============> Private (Should not be used directly) <===============
def _handle_message_event(json_data):
  # (1) Trích xuất tin nhắn từ channel nguồn
  channel_id = json_data['event'].get('channel', '')
  if database_service.is_channel_jp(channel_id) == False:
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

  # (2) Log thông tin của tin nhắn đã gửi (là tin nhắn mới hay là update)
  log(f"""
Received message: {message_text}
ts = {ts}
channel_id = {channel_id}
is_edited = {is_edited}
channel_vn = {channel_vn}
message_ts_vn = {message_ts_vn}
message_ts_vn_type = {type(message_ts_vn)}
""")

  # (3) Gửi thông tin chat cho Open API
  gpt_reply = chatgpt_service.request_text(
      database_service.get_system_rule(channel_id),
      database_service.get_assistant_rule(channel_id),
      message_text
  )

  try:
    # (4) Nhận show log thông tin đã phản hồi từ Open API
    log(f'gpt_reply = {gpt_reply}')

    # (5) Gửi thông tin về cho target thread
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

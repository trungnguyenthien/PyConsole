# views.py
from ..utils.log import log
from django.http import JsonResponse
import json
from ..service import slack as slack_service
from ..service import database as database_service
from ..service import chatgpt as chatgpt_service
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
        return handle_message_event(json_data)

    return repsponse_to_slack_received_event

def handle_message_event(json_data):
    # Trích xuất và log tin nhắn
    channel_id = json_data['event'].get('channel', '')
    event_ts = json_data['event'].get('ts', '')
    
    if database_service.tracked_event(channel_id, event_ts):
        return repsponse_to_slack_received_event
    
    
    log(f'handle_message_event CHANNEL_ID = {channel_id}')
    if database_service.is_channel_jp(channel_id) == False:
        log(f'MESSAGE FROM  VN_CHANNEL --> SKIP')
        return repsponse_to_slack_received_event
    
    channel_jp = channel_id
    
    try:
        message_text = json_data['event']['message'].get('text', '')
        jp_ts = json_data['event']['message'].get('ts', '')
        is_edited = True
    except:
        jp_ts = json_data['event'].get('ts', '')
        message_text = json_data['event'].get('text', '')
        is_edited = False
    
    log(f'is_channel_jp = {True}')
    channel_vn = database_service.get_channel_vn(channel_jp)
    log(f'channel_vn = {channel_vn}')
    vn_ts = database_service.get_message_ts_vn(channel_jp, jp_ts)
    log(f"""
Received message: {message_text}
jp_ts = {jp_ts}
channel_jp = {channel_jp}
is_edited = {is_edited}
channel_vn = {channel_vn}
vn_ts = {vn_ts}
message_ts_vn_type = {type(vn_ts)}
""")
    gpt_reply = chatgpt_service.request_text(
        database_service.get_system_rule(channel_jp),
        message_text
    )

    if is_complex_content(gpt_reply):
        summary = chatgpt_service.request_text(
            """
- Hãy tóm tắt các ý chính của nội dung dưới đây, chú ý các cột mốc về thời gian. 
- Mỗi ý là một dòng ngắn.""",
            gpt_reply
        )
        gpt_reply = f""""{gpt_reply}
----------------------------------------------------------------
*🤖 CÁC Ý CHÍNH 🤖*
{summary}"""
        gpt_reply = f'🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳\n{gpt_reply}'
    try:
        log(f'gpt_reply = {gpt_reply}')
        if is_edited:
            vn_ts = slack_service.update_message(channel_vn, vn_ts, gpt_reply)
        else:
            vn_ts = slack_service.send_new_message(channel_vn, gpt_reply)
        log(f'Message has beed sent to vn_channel')
    except Exception as e:
        log(f"manager/slack.py>> Error occurred: {e}")
    
    database_service.save_message_ts_vn(channel_id, channel_vn, jp_ts, vn_ts)
    
    return repsponse_to_slack_received_event
# BOT FUNCTIONS ----------------------------------------------------------------

def is_complex_content(content_string):
    # Tách chuỗi thành một list các từ
    words = content_string.split()
    # Kiểm tra nếu số lượng từ nhiều hơn 300
    return len(words) > 100

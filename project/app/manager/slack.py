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
ts_dict_jp_vn = {}


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
    event_ts = json_data.get('event_id', '')
    
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



# SLACK_BOT FUNCTIONS ----------------------------------------------------------------


def adapt_handle_message_event_for_sub_messages(json_body, channel_vn, text):
    type, message_ts, thread_ts, _ = message_type(json_body)
    log(f"checking message type: {type} ts = {message_ts}")

    if type == 1:
        response = slack_service.send_new_message(channel_vn, text)
        ts_dict_jp_vn[message_ts] = get_vn_ts(response)
    if type == 2:
        thread_ts_vn = ts_dict_jp_vn.get(thread_ts)
        if thread_ts_vn is not None:
            response = slack_service.send_sub_message(
                channel_vn, thread_ts_vn, text)
            ts_dict_jp_vn[message_ts] = get_vn_ts(response)
    # TODO: if type == 3: # Use to edit main message
    #     response = send_new_message(channel_vn, gpt_reply)
    #     ts_dict_jp_vn[message_ts] = get_vn_ts(response)
    if type == 4:
        message_ts_vn = ts_dict_jp_vn.get(message_ts)
        if message_ts_vn is not None:
            response = slack_service.update_message(
                channel_vn, message_ts_vn, text)


def message_type(json_body):
    event = json_body["event"]

    type = event["type"]
    parent_user_id = event.get("parent_user_id")
    previous_message = event.get("previous_message")

    if type != "message":
        return -1, None, None, None
    if previous_message is not None:
        ts = event.get("message").get("ts")
        thread_ts = event.get("message").get("thread_ts")
        text = event.get("message").get("text")
        return 4, ts, thread_ts, text  # Update sub message
    if parent_user_id is not None:
        ts = event.get("ts")
        thread_ts = event.get("thread_ts")
        text = event.get("text")
        return 2, ts, thread_ts, text  # Create sub message
    # TODO: if ... return 3 # Use to edit main message
    ts = event.get("ts")
    text = event.get("text")
    return 1, ts, None, text  # Create new


def get_vn_ts(response):
    return response["ts"]

# BOT FUNCTIONS ----------------------------------------------------------------

def is_complex_content(content_string):
    # Tách chuỗi thành một list các từ
    words = content_string.split()
    # Kiểm tra nếu số lượng từ nhiều hơn 300
    return len(words) > 100

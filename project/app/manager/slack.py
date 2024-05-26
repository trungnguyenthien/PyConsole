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


def adapt_handle_message_event_for_sub_messages(json_body, vn_channel, ai_text):
    mssg_type, jp_message_timestamp, jp_parent_message_timestamp, text = message_type_v2(
        json_body)

    if mssg_type == 1:  # create new main message
        response = slack_service.send_new_message(vn_channel, text)
        vn_message_timestamp = response.get("ts")
        save_timestamp(jp_message_timestamp, vn_message_timestamp)

    if mssg_type == 2:  # create new sub message
        vn_parent_message_timestamp = get_vn_timestamp(
            jp_parent_message_timestamp)
        if vn_parent_message_timestamp is not None:
            response = get_vn_timestamp(
                vn_channel, vn_parent_message_timestamp, text)
            vn_message_timestamp = response.get("ts")
            save_timestamp(jp_message_timestamp, vn_message_timestamp)

    if mssg_type == 3:  # edit message
        jp_previous_message_timestamp = jp_message_timestamp
        vn_previous_message_timestamp = get_vn_timestamp(
            jp_previous_message_timestamp)
        if vn_previous_message_timestamp is not None:
            response = slack_service.update_message(
                vn_channel, vn_previous_message_timestamp, text)


def message_type_v2(json_body):
    # @return: message_type, message_timestamp, parent_message_timestamp, text
    ####### message_type #######
    # -1: no action
    # 1 : create new main message
    # 2 : create new sub message
    # 3 : edit message
    # 4 : delete message (TODO: delete main and delete sub)
    ############################
    event = json_body["event"]

    type = event.get("type")
    subtype = event.get("subtype")

    parent_message_timestamp = event.get("thread_ts")

    # (-1) no action
    if type != "message":
        return -1, None, None, None

    # (3) edit message
    if subtype == "message_changed":
        previous_message_timestamp = event.get("message").get(
            "ts")  # or event.get("previous_message").get("ts")
        text = event.get("message").get("text")
        return 3, previous_message_timestamp, None, text

    # (1) create new main message
    if parent_message_timestamp is None:
        message_timestamp = event.get("ts")
        text = event.get("text")
        return 1, message_timestamp, None, text

    # (2) create new sub message
    text = event.get("text")
    message_timestamp = event.get("ts")
    return 2, message_timestamp, parent_message_timestamp, text


def save_timestamp(jp_msg_ts, vn_msg_ts):
    # TODO: Save to database for {key: value} with {jp_message_timestamp: vn_message_timestamp}
    if vn_msg_ts is not None:
        ts_dict_jp_vn[jp_msg_ts] = vn_msg_ts


def get_vn_timestamp(jp_msg_ts):
    # TODO: Get from database key = jp_message_timestamp
    return ts_dict_jp_vn[jp_msg_ts]

# BOT FUNCTIONS ----------------------------------------------------------------


def is_complex_content(content_string):
    # Tách chuỗi thành một list các từ
    words = content_string.split()
    # Kiểm tra nếu số lượng từ nhiều hơn 300
    return len(words) > 100

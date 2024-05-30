# views.py
from ..utils.log import log
from django.http import JsonResponse
import json
from ..service import slack as slack_service
from ..service import database as database_service
from ..service import chatgpt as chatgpt_service
from urllib.parse import urlparse
from urllib.parse import parse_qs

# from asgiref.sync import sync_to_async

# async_request_text = sync_to_async(chatgpt_service.request_text, thread_sensitive=False)

response_to_slack_received_event = JsonResponse({'status': 'ok'}, status=200)
# TODO: Just be a draft values for working-around (Need to be change to use splash command)
summary_command_list = ["@bot_magic", "@comter", "@MyComter"]


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

    return response_to_slack_received_event

def handle_message_event(json_data):
    log("ENTER handle_message_event")
    channel_id = json_data['event'].get('channel', '')
    event_ts = json_data.get('event_id', '')
    if database_service.tracked_event(channel_id, event_ts):
        return response_to_slack_received_event

    # Log thông tin channel
    log(f'handle_message_event CHANNEL_ID = {channel_id}')
    if database_service.is_channel_jp(channel_id) == False:
        log(f'MESSAGE FROM  VN_CHANNEL --> SKIP (but action command)')
        handle_command_action(json_data)
        return response_to_slack_received_event

    jp_channel = channel_id
    log(f'is_jp_channel = {True}')
    vn_channel = database_service.get_channel_vn(jp_channel)
    log(f'vn_channel = {vn_channel}')

    # Handle action
    handle_complex_action(json_data, jp_channel, vn_channel, )

    return response_to_slack_received_event


# SLACK_BOT FUNCTIONS ----------------------------------------------------------------


def handle_complex_action(json_body, jp_channel, vn_channel):
    log("ENTER handle_complex_action")
    mssg_type, jp_message_timestamp, jp_parent_message_timestamp, message_text = message_type_v2(
        json_body)
    user = ''
    try:
        user = json_body['event'].get('user', '')
        if user == '':
            user = json_body['event']['message'].get('user', '')
    except:
        pass
    
    gpt_reply = get_assistant_message(jp_channel, vn_channel, message_text,
                                      jp_message_timestamp, mssg_type == 3, user)

    try:
        log(f'gpt_reply = {gpt_reply}')

        if mssg_type == 1:  # create new main message
            response = slack_service.send_new_message(vn_channel, gpt_reply)
            vn_message_timestamp = response.get("ts")
            save_timestamp(jp_channel, vn_channel,
                           jp_message_timestamp, vn_message_timestamp)

        if mssg_type == 2:  # create new sub message
            vn_parent_message_timestamp = get_vn_timestamp(jp_channel,
                                                           jp_parent_message_timestamp)
            if vn_parent_message_timestamp is not None:
                response = slack_service.send_sub_message(
                    vn_channel, vn_parent_message_timestamp, gpt_reply)
                vn_message_timestamp = response.get("ts")
                save_timestamp(jp_channel, vn_channel,
                               jp_message_timestamp, vn_message_timestamp)

        if mssg_type == 3:  # edit message
            jp_previous_message_timestamp = jp_message_timestamp
            vn_previous_message_timestamp = get_vn_timestamp(jp_channel,
                                                             jp_previous_message_timestamp)
            if vn_previous_message_timestamp is not None:
                response = slack_service.update_message(
                    vn_channel, vn_previous_message_timestamp, gpt_reply)

        if mssg_type == 4:  # delete message
            jp_deleted_message_timestamp = jp_message_timestamp
            vn_deleted_message_timestamp = get_vn_timestamp(jp_channel,
                                                            jp_deleted_message_timestamp)
            if vn_deleted_message_timestamp is not None:
                response = slack_service.delete_message(
                    vn_channel, vn_deleted_message_timestamp)

        log(f'Message has beed sent to vn_channel')
    except Exception as e:
        log(f"manager/slack.py>> Error occurred: {e}")


def get_assistant_message(jp_channel, vn_channel, message_text, jp_ts, is_edited, user):
    if user != '':
        user = f':speech_balloon:<@{user}>:speech_balloon:'
    log("ENTER get_assistant_message")
    log(f'is_channel_jp = {True}')
    vn_channel = database_service.get_channel_vn(jp_channel)
    log(f'vn_channel = {vn_channel}')
    vn_ts = database_service.get_message_ts_vn(jp_channel, jp_ts)
    log(f"""
Received message: {message_text}
jp_ts = {jp_ts}
channel_jp = {jp_channel}
is_edited = {is_edited}
channel_vn = {vn_channel}
vn_ts = {vn_ts}
message_ts_vn_type = {type(vn_ts)}
""")
    gpt_reply = chatgpt_service.request_text(
        database_service.get_system_rule(jp_channel),
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

    return f'🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳\n{user} {gpt_reply}'


def message_type_v2(json_body):
    log("ENTER message_type_v2")
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
        # or event.get("previous_message").get("ts")
        previous_message_timestamp = event.get("message").get(
            "ts")
        text = event.get("message").get("text")
        return 3, previous_message_timestamp, None, text

    # (4) delete message
    if subtype == "message_deleted":
        # or event.get("previous_message").get("ts")
        message_deleted_timestamp = event.get("deleted_ts")
        return 4, message_deleted_timestamp, None, None

    # (1) create new main message
    if parent_message_timestamp is None:
        message_timestamp = event.get("ts")
        text = event.get("text")
        return 1, message_timestamp, None, text

    # (2) create new sub message
    text = event.get("text")
    message_timestamp = event.get("ts")
    return 2, message_timestamp, parent_message_timestamp, text


def save_timestamp(jp_channel_id, vn_channel_id, jp_msg_ts, vn_msg_ts):
    if vn_msg_ts is not None:
        database_service.save_message_ts_vn(
            jp_channel_id, vn_channel_id, jp_msg_ts, vn_msg_ts)


def get_vn_timestamp(jp_channel_id, jp_msg_ts):
    return database_service.get_message_ts_vn(jp_channel_id, jp_msg_ts)

# SLACK_BOT COMMAND FUNCTIONS ----------------------------------------------------------------


def handle_command_action(json_body):
    # (1) get command type and attributes
    command_type, request_channel, request_ts, attributes = get_command_attributes(
        json_body)
    if command_type == 1:
        summaries_conversations(request_channel, request_ts, attributes)


def summaries_conversations(request_channel, request_ts, attributes):
    if len(attributes) < 1:
        return

    # (1) get link that's using for summarizaion
    link = attributes[0]

    # (2) get source channel and thread_ts
    source_channel, thread_ts = get_thread_ts_source_channel(link)

    # (3) collect all conversions from source channel
    conversations = collect_conversations(source_channel, thread_ts)
    if not conversations:
        return

    # (4) request chat_gpt to translate
    gpt_reply = get_assistant_summarization(
        request_channel, request_ts, conversations)

    try:
        log(f'gpt_reply = {gpt_reply}')

        # (5) send back to request thread as sub message
        slack_service.send_sub_message(
            request_channel, request_ts, gpt_reply)

        log(f'Message has beed sent to vn_channel')
    except Exception as e:
        log(f"manager/slack.py>> Error occurred: {e}")


def collect_conversations(source_channel, thread_ts):
    response = slack_service.get_all_conversions(source_channel, thread_ts)
    all_messages = []
    for item in response.data["messages"]:
        # ts = item.get("ts")
        thread_ts = item.get("thread_ts")
        text = item.get("text")
        all_messages.append(f"- {text}")

    message = "\n".join(all_messages)
    return message


# --> 1: Summary action
def get_command_attributes(json_data):
    event = json_data["event"]

    command_raw = event.get("text")
    request_channel = event.get("channel")
    request_ts = event.get("ts")
    components = command_raw.split(" ")
    if len(components) < 2:
        return -1, request_channel, request_ts, []

    command_type = components[0]
    if command_type in summary_command_list:
        attributes = components[1:]
        return 1, request_channel, request_ts, attributes

    return -1, request_channel, request_ts, []


# i.e: <https://ntrung.slack.com/archives/C071P11UWHJ/p1716857049521879?thread_ts=1716856857.662559&cid=C071P11UWHJ>
def get_thread_ts_source_channel(link):
    link = link.replace("&amp;", "&")
    link = link.replace("<", "")
    link = link.replace(">", "")

    parsed_url = urlparse(link)
    parsed_qs = parse_qs(parsed_url.query)
    thread_ts = parsed_qs['thread_ts'][0]
    source_channel = parsed_qs['cid'][0]

    return source_channel, thread_ts

# TEMPLATE FUNCTIONS ----------------------------------------------------------------


def get_assistant_summarization(request_channel, request_ts, message_text):
    log(f"""
Received message: {message_text}
From channel = {request_channel}
From ts = {request_ts}
""")

    gpt_reply = chatgpt_service.request_text(
        """
- Hãy dịch đoạn hội thoại bên dưới.
- Sau khi dịch xong hãy tổng hợp lại theo định dạng như bên dưới:
🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳----- Translate -----🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳
{Nội dung dịch}
----------------------------------------------------------------
*🤖 CÁC Ý CHÍNH 🤖*
{Nội dung tóm tắt}
""",
        message_text
    )

    return gpt_reply

# BOT FUNCTIONS ----------------------------------------------------------------


def is_complex_content(content_string):
    # Tách chuỗi thành một list các từ
    words = content_string.split()
    # Kiểm tra nếu số lượng từ nhiều hơn 300
    return len(words) > 100

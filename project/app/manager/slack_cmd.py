# views.py
from ..utils.log import log
from django.http import JsonResponse
import json
from ..service import slack as slack_service
from ..service import database as database_service
from ..service import chatgpt as chatgpt_service
from urllib.parse import urlparse
from urllib.parse import parse_qs
import urllib.parse
# from asgiref.sync import sync_to_async

# async_request_text = sync_to_async(chatgpt_service.request_text, thread_sensitive=False)

response_to_slack_received_event = JsonResponse({'status': 'ok'}, status=200)
# TODO: Just be a draft values for working-around (Need to be change to use splash command)
summary_command_list = ["@bot_magic", "@comter", "@MyComter"]


def slack_summary(request):
    body = request.body.decode("utf-8")
    body_dict = dict(item.split("=") for item in body.split("&"))
    headers = dict(request.headers)
    log("EVENT HEADER\n" + json.dumps(headers, indent=2))
    log("EVENT POSTBODY\n" + json.dumps(body_dict, indent=2))
    request_channel = body_dict['channel_id']
    text = body_dict['text']
    try:
       source_channel, thread_ts = get_thread_ts_source_channel(text)
    except Exception as e:
        log(f"Error updating message: {e}")
        return JsonResponse({"response_type": "in_channel","text": "Định dạng yêu cầu không đúng format"})
    summaries_conversations(text, request_channel, source_channel, thread_ts)
    return JsonResponse({"response_type": "in_channel"}, status=200)

'''
SAMPLE body_dict

{
  'team_id': 'TAGSCCP7Z',
  'team_domain': 'ntrung',
  'channel_id': 'C071P11UWHJ',
  'channel_name': 'jp_channel',
  'user_id': 'UAF8W1P33',
  'user_name': 'ngthientrung',
  'command': '%2Fsummary',
  'text': 'llll',
  'api_app_id': 'A071NP30LCU',
  'is_enterprise_install': 'false',
}

'''


def summaries_conversations(link, request_channel, source_channel, thread_ts):
    # (3) collect all conversions from source channel
    conversations = collect_conversations(source_channel, thread_ts)
    if not conversations:
        return

    # (4) request chat_gpt to translate
    gpt_reply = get_assistant_summarization(conversations)
    # return gpt_reply
    try:
        log(f'gpt_reply = {gpt_reply}')

        # (5) send back to request thread as sub message
        slack_service.send_new_message(request_channel, f"""🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳🇻🇳
Dưới đây là nội dung tóm tắt từ [thread]({link})
*🤖 CÁC Ý CHÍNH 🤖*
{gpt_reply}
""")

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


# i.e: <https://ntrung.slack.com/archives/C071P11UWHJ/p1716857049521879?thread_ts=1716856857.662559&cid=C071P11UWHJ>
def get_thread_ts_source_channel(link):
    link = urllib.parse.unquote(link)
    parsed_url = urlparse(link)
    parsed_qs = parse_qs(parsed_url.query)
    thread_ts = parsed_qs['thread_ts'][0]
    source_channel = parsed_qs['cid'][0]

    return source_channel, thread_ts

# TEMPLATE FUNCTIONS ----------------------------------------------------------------


def get_assistant_summarization(message_text):
    return chatgpt_service.request_text(
        """
- Hãy tóm tắt các ý chính của nội dung dưới đây, chú ý các cột mốc về thời gian. 
- Mỗi ý là một dòng ngắn.
""",message_text)

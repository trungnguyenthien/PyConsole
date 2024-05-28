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


def slack_summary(request):
    body = request.body.decode("utf-8")
    body_dict = dict(item.split("=") for item in body.split("&"))
    headers = dict(request.headers)
    log("EVENT HEADER\n" + json.dumps(headers, indent=2))
    log("EVENT POSTBODY\n" + json.dumps(body_dict, indent=2))
    
    text = body_dict['text']
    
    return response_to_slack_received_event

'''
SAMPLE body_dict

{
  'token': 'OifjAOHsLCZZ3u8wvqUF4o7s',
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
  'response_url': 'https%3A%2F%2Fhooks.slack.com%2Fcommands%2FTAGSCCP7Z%2F7187489248834%2F3nnoeuKaCRtzNIdwwhxSeAdR',
  'trigger_id': '7200157835345.356896431271.03a872a87805c05d3cc17baeb74e1d74'
}

'''
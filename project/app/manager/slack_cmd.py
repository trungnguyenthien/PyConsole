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
    # Lấy dữ liệu từ yêu cầu Slack và giải mã từ UTF-8
    # try:
    #    log("EVENT POSTBODY\n" + json.dumps(request.body, indent=2))
    # except Exception as e:
    #     log(f"Error updating message: {e.response['error']}")

    body = request.body.decode("utf-8")
    headers = dict(request.headers)
    log("EVENT HEADER\n" + json.dumps(headers, indent=2))
    log("EVENT POSTBODY\n" + body)
    json_data = json.loads(body)

    # Kiểm tra loại sự kiện
    if 'type' in json_data and json_data['type'] == 'url_verification':
        # Trả lại challenge code mà Slack gửi
        return JsonResponse({'challenge': json_data['challenge']})
    return response_to_slack_received_event
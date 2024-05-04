# views.py
from django.http import HttpResponse
from ..utils.log import log
from django.http import JsonResponse
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

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
        log("EVENT MESSAGE")
        return _handle_message_event(json_data)
    else:
        return HttpResponse("NOT YET HANDLE THIS EVENT", status=200)

def _handle_message_event(json_data):
    # Trích xuất và log tin nhắn
    message_text = json_data['event']["message"].get('text', 'No message text provided')
    log("Received message: " + message_text)
    return HttpResponse("OK", status=200)

### BOT FUNCTIONS ----------------------------------------------------------------
client = WebClient(token='xoxb-356896431271-7054590596066-8JWCx92HQecY7RiovsecRaXY')

# Example usage:
# update_message('C1234567890', '1234567890.123456', 'This is the new message content')
def update_message(channel_id, ts, new_message):
    try:
        response = client.chat_update(
            channel=channel_id,
            ts=ts,
            text=new_message
        )
        log(["Message updated successfully:", response['message']['text']])
    except SlackApiError as e:
        log(f"Error updating message: {e.response['error']}")


# Example usage:
# send_new_message('C1234567890', 'Hello, world!')
def send_new_message(channel_id, message):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        log(["Message sent successfully:", response['message']['text']])
    except SlackApiError as e:
        log(f"Error sending message: {e.response['error']}")
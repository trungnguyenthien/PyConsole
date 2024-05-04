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
        return handle_message_event(json_data)
    else:
        return HttpResponse("NOT YET HANDLE THIS EVENT", status=200)

def handle_message_event(json_data):
    log("EVENT MESSAGE 1")
    # Trích xuất và log tin nhắn
    channel_id = json_data.get('team_id', '')
    
    try:
        message_text = json_data['event']['message'].get('text', '')
        ts = json_data['event']['message']['edited'].get('ts', '')
        is_edited = True
    except:
        ts = json_data['event'].get('ts', '')
        message_text = json_data['event'].get('text', '')
        is_edited = False
    
    log(f"Received message: {message_text} \n ts = {ts} \n channel_id = {channel_id} \n is_edited = {is_edited}")
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
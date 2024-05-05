
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from ..utils.log import log

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
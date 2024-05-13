
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from ..utils.log import log
from ..utils import secret
import json

client = WebClient(token = secret.slack_bot_token)

def update_message(channel_id, ts, new_message):
    # Example usage:
    # update_message('C1234567890', '1234567890.123456', 'This is the new message content')
    log(f'update_message({channel_id}, {ts}, {new_message})')
    try:
        response = client.chat_update(
            channel=channel_id,
            ts=ts,
            text=new_message
        )
        log(f'chat_update response = {json.dumps(response)}')
        log(["Message updated successfully:", response['message']['text']])
    except SlackApiError as e:
        log(f"Error updating message: {e.response['error']}")

def send_new_message(channel_id, message):
    # Example usage:
    # send_new_message('C1234567890', 'Hello, world!')
    log(f'send_new_message({channel_id}, {message})')
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        log(f'send_new_message response = {json.dumps(response)}')
        log(["Message sent successfully:", response['message']['text']])
    except SlackApiError as e:
        log(f"Error sending message: {e.response['error']}")
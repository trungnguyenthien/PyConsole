
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from ..utils.log import log
from . import secret as secret_service

client = WebClient(token = secret_service.slack_bot_token)

def update_message(channel_id, ts, new_message):
    # Example usage:
    # update_message('C1234567890', '1234567890.123456', 'This is the new message content')
    try:
        response = client.chat_update(
            channel=channel_id,
            ts=ts,
            text=new_message
        )
        log(["Message updated successfully:", response['message']['text']])
    except SlackApiError as e:
        log(f"Error updating message: {e.response['error']}")

def send_new_message(channel_id, message):
    # Example usage:
    # send_new_message('C1234567890', 'Hello, world!')
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        log(["Message sent successfully:", response['message']['text']])
    except SlackApiError as e:
        log(f"Error sending message: {e.response['error']}")
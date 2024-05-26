
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from ..utils.log import log
from ..utils import secret
from ..utils.common import json_object

client = WebClient(token=secret.slack_bot_token)


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
        log(f'chat_update response = {json_object(response)}')
        log(["Message updated successfully:", response['message']['text']])
        return response
    except SlackApiError as e:
        log(f"Error updating message: {e.response['error']}")
    return None


def send_new_message(channel_id, message):
    # Example usage:
    # send_new_message('C1234567890', 'Hello, world!')
    log(f'send_new_message({channel_id}, {message})')
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        log(f'send_new_message response = {json_object(response)}')
        log(["Message sent successfully:", response['message']['text']])
        return response
    except SlackApiError as e:
        log(f"Error sending message: {e.response['error']}")

    return None


def send_sub_message(channel_id, thread_ts, message):
    # Example usage:
    # send_new_message('C1234567890', '1715405022.898079', 'Hello, world!')
    log(f'send_sub_message({channel_id}, {thread_ts}, {message})')
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message,
            thread_ts=thread_ts
        )
        log(["Message sent successfully:", response['message']['text']])
        return response
    except SlackApiError as e:
        log(f"Error sending message: {e.response['error']}")


def delete_message(channel_id, message_id):
    # Example usage:
    # delete_message('C1234567890', '1714993823.193669')
    log(f'delete_message({channel_id}, {message_id})')
    try:
        # Call the chat.chatDelete method using the built-in WebClient
        response = client.chat_delete(
            channel=channel_id,
            ts=message_id
        )
        log(["Message delete successfully:", response])
        return response
    except SlackApiError as e:
        log(f"Error delete message: {e.response['error']}")


def all_conversions(channel_id, message_id):
    # Cần phải add con bot vào channel cần lấy message
    # Example usage:
    # all_conversions('C1234567890', '1714993823.193669')
    print(f'all_conversions({channel_id}, {message_id})')
    try:
        # Call the chat.chatDelete method using the built-in WebClient
        response = client.conversations_replies(
            channel=channel_id,
            ts=message_id
        )
        print(["Load message successfully:", response])
        return response
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

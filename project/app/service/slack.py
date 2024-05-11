from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from ..utils.log import log
from ..utils import secret

# ===============> Init <===============
client = WebClient(token=secret.slack_bot_token)

# ===============> Export functions <===============
# Example usage:
# Infor: https://ntrung.slack.com/archives/C071P11UWHJ/p1714993968880839?thread_ts=1714993823.193669&cid=C071P11UWHJ
# Components:
# -----> channel_id: C071P11UWHJ
# -----> ts: 1714993823.193669
# -----> new_message: 'This is the new message content' (Note: Input from user)
"""
Update available message in main thread
@channel_id:    the channel contains message
@ts:            timestampe of the available message of main thread
@new_message:   new message use to override the available message
"""
def update_message(channel_id, ts, new_message):
  log(f'update_message({channel_id}, {ts}, {new_message})')

  try:
    response = client.chat_update(
        channel=channel_id,
        ts=ts,
        text=new_message
    )
    log(["Message updated successfully: ", response['message']['text']])
  except SlackApiError as e:
    log(f"Error updating message: {e.response['error']}")


# Example usage:
# Infor: https://ntrung.slack.com/archives/C071P11UWHJ/p1714993968880839?thread_ts=1714993823.193669&cid=C071P11UWHJ
# Components:
# -----> channel_id: C071P11UWHJ
# -----> message_id: p1714993968880839
# -----> ts: 1714993823.193669
# -----> new_message: 'This is the new message content' (Note: Input from user)
"""
TODO: Update available sub message
@channel_id:    the channel contains message
@ts:            timestampe of the available message of main thread
@ts:            p1714993968880839 ???
@new_message:   new message use to override the available message
"""
def update_sub_message(channel_id, ts, new_message):
  # Example usage:
  # update_message('C1234567890', '1234567890.123456', 'This is the new message content')
  log(f'Comming soon...')


"""
Send new message
@channel_id:    the channel contains message
@new_message:   new message to send
"""
def send_new_message(channel_id, message):
  # Example usage:
  # send_new_message('C1234567890', 'Hello, world!')
  log(f'send_new_message({channel_id}, {message})')
  try:
    response = client.chat_postMessage(
        channel=channel_id,
        text=message
    )
    log(["Message sent successfully:", response['message']['text']])
  except SlackApiError as e:
    log(f"Error sending message: {e.response['error']}")

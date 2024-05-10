
channels = [
    {"jp": "C071P11UWHJ", "vn": "C071ZS2BH5G"}
]

def is_channel_jp(channel_id):
  for channel in channels:
    if channel['jp'] == channel_id:
      return True
  return False

def get_channel_vn(channel_jp):
  for channel in channels:
    if channel['jp'] == channel_jp:
      return channel['vn']
  return ""

def update_message_ts_vn(channel_jp, message_ts_jp, message_ts_vn):
  return ""

def get_message_ts_vn(channel_jp, message_ts_jp):
  return None

def get_system_rule(channel_jp):
  return [
      """Bạn là một trợ lý đắc lực trong channel Slack. 
Công việc của bạn là truyền đạt đầy đủ nội dung từ Tiếng Anh sang Tiếng Việt."""
  ]


def get_assistant_rule(channel_jp):
  return [
      "Trong quá trình dịch hãy giữ nguyên định dạng MarkDown của message"
  ]


def get_channel_vn(channel_jp):
  return ""

def get_message_ts_vn(channel_jp, message_ts_jp):
  return ""

def get_system_rule(channel_jp):
  return [
"""
Bạn là một trợ lý đắc lực trong channel Slack. 
Công việc của bạn là truyền đạt đầy đủ nội dung từ Tiếng Anh sang Tiếng Việt."
"""
  ]


def get_assistant_rule(channel_jp):
  return [
    "Trong quá trình dịch hãy giữ nguyên định dạng MarkDown của message",
    ""
  ]
from ..models import SystemMessageRecord, ChannelTsRecord, LogRecord, TaskRecord
from ..utils.log import log

def is_channel_jp(channel_id):
  log(f'is_channel_jp({channel_id})')
  try:
    record = SystemMessageRecord.objects.filter(cid_jp=channel_id)
  except Exception as e:
        log(f"service/database.py>> Error occurred: {e}")
  # log("is_channel_jp: " + record)
  return record.exists()
    
def get_channel_vn(channel_jp):
  log(f'get_channel_vn({channel_jp})')
  record = SystemMessageRecord.objects.first(cid_jp = channel_jp)
  if record:
    return record.cid_vn
  else:
    return None

def update_message_ts_vn(channel_jp, message_ts_jp, message_ts_vn):
  record = ChannelTsRecord.objects.first(cid_jp = channel_jp, ts_jp = message_ts_jp)
  if record:
    record.ts_vn = message_ts_vn
    record.save()
  else:
    pass

def get_message_ts_vn(channel_jp, message_ts_jp):
  log(f'get_message_ts_vn({message_ts_jp})')
  record = ChannelTsRecord.objects.first(cid_jp = channel_jp, ts_jp = message_ts_jp)
  if record:
    return record.ts_vn
  else:
    return None

def get_system_rule(channel_jp):
  return SystemMessageRecord.objects.get(cid_jp = channel_jp).message


# def get_assistant_rule(channel_jp):
#   return [
#     "Trong quá trình dịch hãy giữ nguyên định dạng MarkDown của message"
#   ]
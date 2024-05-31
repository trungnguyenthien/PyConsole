from ..models import SystemMessageRecord, ChannelTsRecord, LogRecord, TaskRecord, TrackingEventRecord
from ..utils.log import log

def is_channel_jp(channel_id):
  log(f'is_channel_jp({channel_id})')
  try:
    record = SystemMessageRecord.objects.filter(cid_jp=channel_id)
  except Exception as e:
        log(f"service/database.py>> Error occurred: {e}")
  # log("is_channel_jp: " + record)
  return record.exists()

def tracked_event(channel, ts):
  event = f'{channel}_{ts}'
  if TrackingEventRecord.objects.filter(event=event).exists():
    return True
  else:
    TrackingEventRecord(event=event).save()
    return False

def get_channel_vn(channel_jp):
  log(f'get_channel_vn({channel_jp})')
  try:
    record = SystemMessageRecord.objects.filter(cid_jp=channel_jp).first()
    if record:
      return record.cid_vn
    else:
      return None
  except Exception as e:
        log(f"service/database.py>> Error occurred: {e}")
        return None

def save_message_ts_vn(channel_jp, channel_vn, message_ts_jp, message_ts_vn):
  record = ChannelTsRecord.objects.filter(cid_jp = channel_jp, ts_jp = message_ts_jp).first()
  if record is None:
    ChannelTsRecord(cid_jp=channel_jp, cid_vn=channel_vn, ts_jp=message_ts_jp, ts_vn=message_ts_vn).save()
    

def get_message_ts_vn(channel_jp, message_ts_jp):
  log(f'get_message_ts_vn({message_ts_jp})')
  record = ChannelTsRecord.objects.filter(cid_jp = channel_jp, ts_jp = message_ts_jp).first()
  if record:
    return record.ts_vn
  else:
    return None

def get_system_rule(channel_jp):
  return SystemMessageRecord.objects.filter(cid_jp = channel_jp).first().message


# def get_assistant_rule(channel_jp):
#   return [
#     "Trong quá trình dịch hãy giữ nguyên định dạng MarkDown của message"
#   ]
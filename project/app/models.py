from django.db import models
import pytz
from django.utils.timezone import now

def getTime(time):
    return time.strftime("%H:%M:%S")

class SystemMessageRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cid_jp = models.CharField(max_length=12, default='') # Ex: C071P11UWHJ
    cid_vn = models.CharField(max_length=12, default='') # Ex: C071P11UWHJ
    message = models.TextField(default = '')

class ChannelTsRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    cid_jp = models.CharField(max_length=12, default='') # Ex: C071P11UWHJ
    ts_jp = models.CharField(max_length=20, default='') # Ex: 1715040181.995619
    cid_vn = models.CharField(max_length=12, default='') # Ex: C071P11UWHJ
    ts_vn = models.CharField(max_length=20, default='') # Ex: 1715040181.995619

class LogRecord(models.Model):
    created_at = models.DateTimeField(default=now)
    data = models.TextField(default='')
    # type = models.IntegerField(default=0) # 0=info, 1=warning, 2=error

    def to_dict(self):
        return {'timestamp': self.created_at.strftime('%Y-%m-%d %H:%M:%S'), 'data': self.data }

class TaskRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=12)
    data = models.TextField()
    priority = models.IntegerField(default=0) # 0 is highest priority
    open_status = models.BooleanField(default=1) # 0:close, 1:open
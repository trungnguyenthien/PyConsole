from django.db import models
import pytz
from django.utils.timezone import now

# Cho phép team tuỳ chỉnh yêu cầu cách dịch cho Bot
class SystemMessageRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cid_jp = models.CharField(max_length=12, default='') # Ex: C071P11UWHJ
    cid_vn = models.CharField(max_length=12, default='') # Ex: C071P11UWHJ
    message = models.TextField(default = '')

# Lưu lại các event đã được xử lý, reject event  mà slack gửi trùng
class TrackingEventRecord(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=30, default='') # Ex: C071P11UWHJ_1715040181.995619

# Lưu channel và ts của VN và JP
class ChannelTsRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    cid_jp = models.CharField(max_length=12, default='') # Ex: C071P11UWHJ
    ts_jp = models.CharField(max_length=20, default='') # Ex: 1715040181.995619
    cid_vn = models.CharField(max_length=12, default='') # Ex: C071P11UWHJ
    ts_vn = models.CharField(max_length=20, default='') # Ex: 1715040181.995619

# Lưu Log
class LogRecord(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=now)
    data = models.TextField(default='')

    def to_dict(self):
        return {'timestamp': self.created_at.strftime('%Y-%m-%d %H:%M:%S.%f'), 'data': self.data }

# Lưu Task Queue 
class TaskRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=12)
    data = models.TextField()
    priority = models.IntegerField(default=0) # 0 is highest priority
    open_status = models.BooleanField(default=1) # 0:close, 1:open
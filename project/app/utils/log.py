from ..models import SystemMessageRecord, ChannelTsRecord, LogRecord, TaskRecord


# _log_queue = []

from datetime import datetime


def all_logs():
    # Tạo bản sao của _log_queue và đảo ngược thứ tự của các phần tử
    return LogRecord.objects.all().order_by('-created_at')

_limit_log = 100
def log(data, created_at = datetime.now()):
    # TODO: insert thêm logRecord vào, nếu số log nhiều hơn _limit_log thì xoá bớt log đã lưu lâu nhất (dựa vào created_at)
    # Thêm một bản ghi log mới
    LogRecord.objects.create(content=data, type=type, created_at=created_at)

    # Kiểm tra số lượng logs hiện tại
    current_log_count = LogRecord.objects.count()
    if current_log_count > _limit_log:
        # Tính số logs cần xóa
        logs_to_delete = current_log_count - _limit_log

        # Tìm và xóa các logs cũ nhất
        oldest_ids = LogRecord.objects.all().order_by('created_at')[:logs_to_delete].values_list('id', flat=True)
        LogRecord.objects.filter(id__in=list(oldest_ids)).delete()

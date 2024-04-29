
_limit_log = 100
_log_queue = []

def all_logs():
    # Hàm này cho phép truy cập an toàn đến log_queue từ bên ngoài
    return _log_queue.copy()

def log(data):
    while len(_log_queue) >= _limit_log:
        # Xóa phần tử đầu tiên nếu số lượng phần tử vượt quá giới hạn
        _log_queue.pop(0)
    # Thêm dữ liệu mới vào cuối của _log_queue
    _log_queue.append(data)

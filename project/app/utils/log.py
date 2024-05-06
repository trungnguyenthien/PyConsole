
_limit_log = 100
_log_queue = []

from datetime import datetime

def getTime(time):
    return time.strftime("%H:%M:%S")

class LogItem:
    def __init__(self, timestamp, request_time, data):
        self.timestamp = timestamp      # Thời gian ghi log
        self.request_time = request_time  # Timestamp của request
        self.data = data                # Dữ liệu có thể là kiểu bất kỳ

    def to_dict(self):
        return {
            'timestamp': getTime(self.timestamp),
            'request_time': getTime(self.request_time),
            'data': self.data  # Giả sử rằng data đã là kiểu có thể serialize được, nếu không bạn cần xử lý thêm
        }           # Dữ liệu có thể là kiểu bất kỳ

    def __str__(self):
        return f"LogItem(timestamp={self.timestamp}, request_time={self.request_time}, data={self.data})"

def all_logs():
    # Tạo bản sao của _log_queue và đảo ngược thứ tự của các phần tử
    reversed_queue = _log_queue.copy()
    reversed_queue.reverse()
    return reversed_queue

def log(data, request_time = datetime.now()):
    # while len(_log_queue) >= _limit_log:
    #     # Xóa phần tử đầu tiên nếu số lượng phần tử vượt quá giới hạn
    #     _log_queue.pop(0)
    # Thêm dữ liệu mới vào cuối của _log_queue
    _log_queue.append(LogItem(datetime.now(), request_time, data))
    print(data)

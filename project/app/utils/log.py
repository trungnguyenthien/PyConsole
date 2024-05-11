from datetime import datetime
_limit_log = 100
_log_queue = []

# ===============> Exported functions <===============
"""
Show all added logs
@return: _log_queue in reverse
"""
def all_logs():
  # Tạo bản sao của _log_queue và đảo ngược thứ tự của các phần tử
  reversed_queue = _log_queue.copy()
  reversed_queue.reverse()
  return reversed_queue


"""
Add log to _log_queue
@return: array of _log_queue
"""
def log(data, request_time=datetime.now()):
  while len(_log_queue) >= _limit_log:
    # Xóa phần tử đầu tiên nếu số lượng phần tử vượt quá giới hạn
    _log_queue.pop(0)
  # Thêm dữ liệu mới vào cuối của _log_queue
  _log_queue.append(_LogItem(datetime.now(), request_time, data))
  # print(data) # TẠI SAO LẠI LỖI CHỖ NÀY NÀY????


# ===============> Private (Should not be used directly) <===============
class _LogItem:
  def __init__(self, timestamp, request_time, data):
    self.timestamp = timestamp        # Thời gian ghi log
    self.request_time = request_time  # Timestamp của request
    self.data = data                  # Dữ liệu có thể là kiểu bất kỳ

  # -----> Public functions <-----
  def to_dict(self):
    return {
        'timestamp': self.__getTime(self.timestamp),
        'request_time': self.__getTime(self.request_time),
        # Giả sử rằng data đã là kiểu có thể serialize được, nếu không bạn cần xử lý thêm
        'data': self.data  # Dữ liệu có thể là kiểu bất kỳ
    }

  # -----> Private functions <-----
  def __str__(self):
    return f"LogItem(timestamp={self.timestamp}, request_time={self.request_time}, data={self.data})"

  def __getTime(time):
    return time.strftime("%H:%M:%S")

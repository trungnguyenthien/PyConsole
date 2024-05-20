## slack_init_db

- Định nghĩa database để lưu data giữa các phiên làm việc tham khảo models.py
- Dịch và tóm tắt
- Fix lỗi xử lý trùng event (Cần phản hồi event từ slack trong 3s, nếu phản hồi sớm phải lưu lại event_id để reject xử lý lần nhận sau)
- Lưu log giữa các phiên start app

## slack_init_db

- Định nghĩa database để lưu data giữa các phiên làm việc tham khảo models.py
- Dịch và tóm tắt
- Fix lỗi xử lý trùng event (Cần phản hồi event từ slack trong 3s, nếu phản hồi sớm phải lưu lại event_id để reject xử lý lần nhận sau)
- Lưu log giữa các phiên start app

## phhai
dịch được trong sub-message
update/delete nội dung tương ứng
Đã tóm lượt được ý chính trong thread.

## trung-slashcmd
Đã thực hiện hiện được command như dưới đây
```
/summary https://ntrung.slack.com/archives/C071P11UWHJ/p1716857049521879?thread_ts=1716856857.662559&cid=C071P11UWHJ
```
Issue: do xử lý đồng bộ nên SlackBot sẽ có thông báo operation_timeout xuất hiện.
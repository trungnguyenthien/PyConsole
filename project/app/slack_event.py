# views.py
from django.http import HttpResponse
from slack_sdk.signature import SignatureVerifier
from slack_sdk.errors import SlackRequestError
from .log import log

# Thay thế bằng Signing Secret của ứng dụng Slack
SLACK_SIGNING_SECRET = "aaf005f370e572a9a98951d01dcf146e"

# Tạo đối tượng SignatureVerifier
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

def slack_events(request):
    # Lấy dữ liệu từ yêu cầu Slack
    body = request.body.decode("utf-8")
    headers = dict(request.headers)
    log(body)

    # Xác minh yêu cầu từ Slack
    try:
        is_valid = signature_verifier.is_valid_request(body, headers)
    except SlackRequestError as e:
        # Xử lý lỗi xác minh
        log(HttpResponse(str(e), status=403))
        return HttpResponse(str(e), status=403)

    if not is_valid:
        # Yêu cầu không hợp lệ
        log(HttpResponse("Invalid request", status=403))
        return HttpResponse("Invalid request", status=403)

    # Xử lý sự kiện xác minh từ Slack
    event = request.GET.get("event", {})
    if "challenge" in event:
        # Gửi phản hồi xác minh
        return HttpResponse(event["challenge"], status=200)

    # Xử lý các sự kiện khác từ Slack
    # ...

    return HttpResponse("OK", status=200)
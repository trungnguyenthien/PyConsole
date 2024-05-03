# views.py
from django.http import HttpResponse
from slack_sdk.signature import SignatureVerifier
from slack_sdk.errors import SlackRequestError
from .log import log
from django.http import JsonResponse
import json

# Thay thế bằng Signing Secret của ứng dụng Slack
SLACK_SIGNING_SECRET = "3135f508999027a39f18c8c0d3a297a0"
# xoxb-356896431271-7054590596066-G0Q4LHfxB1oBXKFxHTFaWmrs

# Tạo đối tượng SignatureVerifier
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

def slack_events(request):
  # Lấy dữ liệu từ yêu cầu Slack
    body = request.body.decode("utf-8")
    headers = dict(request.headers)
    log(body)
    log(headers)

    json_data = json.loads(body)
    
    # Kiểm tra loại sự kiện
    if 'type' in json_data and json_data['type'] == 'url_verification':
        # Trả lại challenge code mà Slack gửi
        return JsonResponse({'challenge': json_data['challenge']})

    # Xử lý các sự kiện khác từ Slack
    # ...

    return HttpResponse("OK", status=200)
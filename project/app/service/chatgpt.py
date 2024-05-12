
from ..utils import secret as secret
from ..utils.log import log
import openai
import json
import codecs

def request_text(system_specs, user_message):
    """
    SAMPLE RESPONSE:
    --------------------------------
    {
    "choices": [
        {
        "finish_reason": "stop",
        "index": 0,
        "message": {
            "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
            "role": "assistant"
        },
        "logprobs": null
        }
    ],
    "created": 1677664795,
    "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
    "model": "gpt-3.5-turbo-0613",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 17,
        "prompt_tokens": 57,
        "total_tokens": 74
    }
    }
    """
    try:
        openai.api_key = secret.openApi_key
        messages = []
        messages.append({"role": "system", "content": """
                        - Bạn là một thông dịch viên trong các cuộc trao đổi trong các công cụ chat.
                        - Bạn chỉ dịch và tóm tắt nội dung của user.
                        - Nếu nội dung không dịch được thì hãy giữ nguyên.
                        - Bạn không cần diễn giải ý nghĩa một từ vựng cho user.
                        - Bạn không cần trả lời bất kỳ câu hỏi nào của user.
        """})
        for content in system_specs:
            messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": user_message})
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = completion.choices[0].message.content
        return reply
    except Exception as e:
        log(f"service/chatgpt.py>> Error occurred: {e}")
        return None  # Return None or handle the error as appropriate for your use case
    
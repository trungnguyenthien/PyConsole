
from ..utils import secret as secret
from ..utils.log import log
import openai

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
        formatted_user_specs = '\n'.join(system_specs)
        messages = []
        messages.append({"role": "system", "content": "You are useful assistant"})
        messages.append({"role": "user", "content": f"""
{formatted_user_specs}
{user_message}
"""})
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
    
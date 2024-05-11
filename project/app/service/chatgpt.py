
from ..utils import secret as secret
from ..utils.log import log
import openai

# ===============> Un-used libraris <===============
# import json
# import codecs

# ===============> Init <===============
openai.api_key = secret.openApi_key
_model = "gpt-4"  # All models at: https://platform.openai.com/docs/models
_max_token = 1000

# ===============> Export functions <===============
"""
Answer the question and get response message from Open API
@return: message from Open API
"""
def request_text(system_specs, assistant_specs, user_message):
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
    # (prepaired step): Create `messages` object that use to send to Open API
    messages = []

    # (1): Add system specs to messages object
    for content in system_specs:
      messages.append({"role": "system", "content": content})

    # (2): Add assistant specs to messages object
    for content in assistant_specs:
      messages.append({"role": "assistant", "content": content})

    # (3): Add all chats of user to messages object
    messages.append({"role": "user", "content": user_message})

    # (4): Send message object to chat gpt model
    completion = openai.chat.completions.create(
        model=_model,
        messages=messages,
        temperature=0.7,
        max_tokens=_max_token,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    reply = completion.choices[0].message.content
    return reply
  except Exception as e:
    log(f"service/chatgpt.py>> Error occurred: {e}")
    return None  # Return None or handle the error as appropriate for your use case


from ..utils import secret as secret
from ..utils import log as logger
import openai

def request_text(system_specs, assistant_specs, user_message):
    openai.api_key = secret.openApi_key
    messages = []
    for content in system_specs:
        messages.append({"role": "system", "content": content})
    for content in assistant_specs:
        messages.append({"role": "assistant", "content": content})
    messages.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    reply = response.choices[0].message["content"]
    return reply
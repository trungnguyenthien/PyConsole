
from ..utils import secret as secret
from ..utils.log import log
import openai
import json
def request_text(system_specs, user_message):
    try:
        openai.api_key = secret.openApi_key
        formatted_user_specs = system_specs
        messages = []
        messages.append({"role": "system", "content": "You are useful assistant"})
        messages.append({"role": "user", "content": f"""
{formatted_user_specs}
----------------------------------------------------------------
{user_message}
"""})
        log(f"""Request to GPT 
{formatted_user_specs}
{user_message}""")

        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = completion.choices[0].message.content
        return reply
    except Exception as e:
        log(f"service/chatgpt.py>> Error occurred: {e}")
        return None  # Return None or handle the error as appropriate for your use case
    
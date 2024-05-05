
from ..utils import secret as secret
from ..utils import log as logger
import openai

openai.api_key = secret.openApi_key

def request_text(system_specs, assistant_specs, user_messages):
  logger.log('request_text')

  messages = []
  for content in system_specs:
    messages.append({"role": "system", "content": content})
  for content in assistant_specs:
    messages.append({"role": "assistant", "content": content})
  for content in user_messages:
    messages.append({"role": "user", "content": content})
  logger.log(f'message = {messages}')
  response = openai.ChatCompletion.create(
    model="gpt-4",  # Sử dụng mô hình GPT-4
    messages=messages,
    temperature=0.7,  # Điều chỉnh độ đa dạng của câu trả lời (0-2)
    max_tokens=10000,  # Giới hạn số lượng token trong câu trả lời
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  reply = response.choices[0].message["content"]
  logger.log(f"Response from OPENAI-------------\n{reply}")
  return reply
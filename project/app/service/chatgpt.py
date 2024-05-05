
from ..utils import secret as secret
from ..utils import log as logger
from openai import OpenAI
from openai import AsyncOpenAI
import aiohttp

# openai.api_key = secret.openApi_key
OpenAI.api_key = secret.openApi_key
client = AsyncOpenAI()

async def request_text(system_specs, assistant_specs, user_message):
    # logger.log(f'request_text key = {openai.api_key}')
    messages = []
    for content in system_specs:
        messages.append({"role": "system", "content": content})
    for content in assistant_specs:
        messages.append({"role": "assistant", "content": content})
    messages.append({"role": "user", "content": user_message})
    logger.log(f'message = {messages}')

    response = await client.chat.completions.create(
            model="gpt-4",  # Sử dụng mô hình GPT-4
            messages=messages,
            # temperature=0.7,  # Điều chỉnh độ đa dạng của câu trả lời (0-2)
            # max_tokens=10000,  # Giới hạn số lượng token trong câu trả lời
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0,
            # request_timeout=60,  # Thời gian chờ tối đa (giây)
        )
    logger.log(f"response-----------\n{response}")
    reply = response.choices[0].message["content"]
    logger.log(f"Response from OPENAI-------------\n{reply}")
    return reply
        
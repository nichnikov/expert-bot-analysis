import os
import sys
import logging
from openai import OpenAI
from dotenv import load_dotenv

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from core.data_definition import Parameters, Settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GPT_Validator:
    def __init__(self, settings: Settings, parameters: Parameters):
        self.prmts = parameters
        self.client = OpenAI(
        api_key=settings.api_key, # ваш ключ в VseGPT после регистрации
        base_url=settings.api_host,)

    def gpt_validation(self, dialogue: str):
        prompt = self.prmts.prompt.format(str(dialogue))

        messages = []
        messages.append({"role": "user", "content": prompt})

        response_big = self.client.chat.completions.create(
            model="openai/gpt-4o-mini", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр openai/gpt-4o-mini
            messages=messages,
            temperature=self.prmts.temperature,
            n=1,
            max_tokens=self.prmts.max_tokens, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
            extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
        )

        #print("Response BIG:",response_big)
        return response_big.choices[0].message.content

    def __call__(self, d: str):
        return self.gpt_validation(d)


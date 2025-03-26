"""Модуль для определения типов данных, используемых в приложении."""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field

# import sys
# sys.path.append("/home/an/Data/github/AITK611-expert-bot-service-with-baai-openai")

class Settings(BaseSettings):
    """Настройки приложения, включая параметры Elasticsearch."""
    es_hosts: str
    es_login: str 
    es_password: str
    openai_api_key: str
    openai_api_host: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



class Parameters(BaseModel):
    """Параметры приложения, включая параметры Elasticsearch и модели."""
    es_request_timeout: int = 100
    es_max_retries: int = 50
    es_retry_on_timeout: bool = True
    es_chunk_size: int = 300
    es_max_hits: int = 30 # 200
    model_name: str = 'BAAI/bge-reranker-large' # '/home/an/.cache/huggingface/hub/models--BAAI--bge-reranker-large'
    device: str = "cuda"
    es_index: str = "ch_documents*" # "ch_documents"  # "publicator_paragraphs*"
    es_first_field: str = "pub_aliases" # "pub_aliases" "sys_ids"
    es_mod_id_name: str = "mod_id" # наименование поля модуля в индексе
    es_doc_id_name: str = "doc_id"  # наименование поля документа в индексе
    es_second_field: str = "text_lem" # "lemmatized_text"
    es_third_field: str = "title_lem" # "lemmatized_text"
    stopwords_files: List[str] = []
    # es_candidates_quantity: int = 30 
    ds_candidates_quantity: int = 10 # количество кандидатов, передающихся для переранжирования
    llm_candidates_quantity: int = 5 # количество кандидатов, передающихся в LLM для отбора лучшего
    ai_model: str ="openai/gpt-4o-mini"
    ai_temperature: float = 0.0
    ai_max_tokens: int = 3000
    ds_rank_score: float = -5.0
    app_name: str = "expert_bot"
    project_host: str = "0.0.0.0"
    project_port: int = 8080
    "module_id", "id"
    alias_to_site: dict = {
        "bss.vip": "https://vip.1gl.ru", 
        "bss": "https://1gl.ru",
        "uss": "https://1jur.ru"
                           }



class PromtsChain(BaseModel):
    validation: str = """
                        Ты опытный бухгалтер, проходящий очень важынй профессиональный тест, критически влияющий на твою карьеру. 
                        В тесте представлен вопрос и варианты бухгалтерских текстов, в которых может быть ответ. 
                        Необходимо выбрать самый лучший текст, отвечающий на вопрос и вернуть его номер. 
                        Верни только номер (цифру) лучшего текста
                        Если в текстах нет ответа на вопрос, то вернуть: "Нет ответа"
                        Вопрос: {}
                        Пронумерованные тексты в которых возможно есть ответ: {}
                        """
    valid_fail: str = "Нет ответа"
    answer_generation: str = """
                            Ты помощник опытного бухгалтера. Тебе нужно очень аккуратно ответить на вопрос клиента.
                            Опытный бухгалтер, твой руководитель, подготовил материал в котором содержится ответ.
                            Тебе нужно прочитать материал и используя его содержание ответить на вопрос.  
                            Вопрос: {}
                            Текст ответа: {}"""


# Модель для входных данных (запроса)
class QueryRequest(BaseModel):
    query: str
    alias: str

# Модель для выходных данных (ответа)
class AnswerResponse(BaseModel):
    answer: str
    answer_text: str
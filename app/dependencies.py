import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)


from core.data_types import Settings, Parameters, PromtsChain
from services.retriever import Retriever
from llm.ai_agent import OpenAIClient, AIAgent
# from services.answer_agent import AnswerAgent
# from services.validate_agent import AnswerAgent
from core.config import logger

mode = "test"
assert mode in ["prod", "test"]

settings = Settings()
parameters = Parameters()
promts = PromtsChain()

if mode == "test":
    parameters.es_index = "results*"
    parameters.es_first_field = "request.chat_id"
    parameters.es_mod_id_name = "mod_id"
    parameters.es_doc_id_name = "doc_id"
    settings.es_hosts = "http://elasticsearch.prod.nlp.aservices.tech:9200" # "http://elasticsearch.dev.nlp.aservices.tech:9200/"


retriever = Retriever(settings, parameters)
openai_client = OpenAIClient(api_key=settings.openai_api_key)
ai_client = AIAgent(ai_client=openai_client, logger=logger)
# answer_agent = AnswerAgent(parameters, ai_client, promts)
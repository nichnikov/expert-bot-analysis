import re

from llm.ai_agent import AIAgent
from core.data_types import Parameters, PromtsChain
from utils.utils import jaccard_similarity


class AnswerAgent:
    def __init__(self, parameters: Parameters, ai_client: AIAgent, promts: PromtsChain):
        self.parameters = parameters
        self.ai_client = ai_client
        self.promts = promts

    def answer_generate(self, query: str, answers_candidates):
        return self.ai_client(self.promts.validation.format(query, answers_candidates), 
                        model=self.parameters.ai_model, 
                        temperature=self.parameters.ai_temperature, 
                        max_tokens=self.parameters.ai_max_tokens)

        
        
    def __call__(self, query, answers_candidates):
        return self.answer_generate(query, answers_candidates)
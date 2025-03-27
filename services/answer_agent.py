import re
import logging

from llm.ai_agent import AIAgent
from core.data_types import Parameters, PromtsChain
from utils.utils import jaccard_similarity


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class AnswerAgent:
    def __init__(self, parameters: Parameters, ai_client: AIAgent, promts: PromtsChain):
        self.parameters = parameters
        self.ai_client = ai_client
        self.promts = promts

    
    def answer_ranking(self, query: str, answers_candidates: list[str]):
        val = self.ai_client(self.promts.validation.format(query, answers_candidates), 
                        model=self.parameters.ai_model, 
                        temperature=self.parameters.ai_temperature, 
                        max_tokens=self.parameters.ai_max_tokens)
        print("Validated Result:", val)
        if re.sub(r"[^\w\s]", "", val.lower()) == self.promts.valid_fail.lower():
            return None
        else:
            try:
                true_text_number = int(re.sub(r"[^\d]", "", val)) - 1
                return true_text_number
            
            except ValueError as e:
                logger.error("ValueError: %s", e)
                return None

            


    def answer_generate(self, query: str, text_with_answers: str):
        answer = self.ai_client(self.promts.answer_generation.format(query, text_with_answers), 
                    model=self.parameters.ai_model, 
                    temperature=self.parameters.ai_temperature, 
                    max_tokens=self.parameters.ai_max_tokens)

        return answer
        

    def rag_answer_generate(self, query: str, answers_candidates: list[str]):
        
        text_num = self.answer_ranking(query, answers_candidates)
        
        if text_num is None:
            return "No Answer", "No Text"
        
        true_text = answers_candidates[text_num]
        answ = self.answer_generate(query, true_text)
        return answ, true_text

        
    def __call__(self, query, answers_candidates):
        return self.rag_answer_generate(query, answers_candidates)
""" 
This module is responsible for the retrieval of the most relevant answers to the user's query.
"""
import os
import sys
import logging

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from core.data_types import Parameters
# from utils.texts_processing import TextsLemmatizer
from retrievals.elastic.es import ElasticClient
from core.data_types import Settings, Parameters
from retrievals.elastic.queries import Match, MatchPhrase, Bool
# from retrievals.dense import DenseRetriever


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self, settings: Settings, parameters: Parameters):
        self.es = ElasticClient(settings, parameters)
        self.parameters = parameters

    async def es_search(self, es_index, es_query):
        # es_query = {"match_phrase": {self.parameters.es_first_field: chat_id}}
        '''
        es_query = {"bool": {"must": 
                             [{"match_phrase": {self.parameters.es_first_field: sys}},
                              {"multi_match" : {"query":   lm_query,
                                               "fields": [self.parameters.es_second_field, self.parameters.es_third_field+"^2"]}}]
                                               }}'''
        '''
        es_query = {"multi_match" : {"query": lm_query,
                                     "fields": [self.parameters.es_second_field, self.parameters.es_third_field+"^2"]}
                                               }'''
        es_docs = await self.es.search_query(es_index, es_query)
        

        # await self.es.close()
        
        if not es_docs: return []
        dicts_ = [d["_source"] for d in es_docs["hits"]["hits"]]

        # выбор уникальных значений в результатах поиска эластика
        dicts_unique_docts = []
        for d in dicts_:
            # Add dictionary if it is not equal to any existing dictionary in the list
            if all(d != existing for existing in dicts_unique_docts):
                dicts_unique_docts.append(d)

        return dicts_unique_docts

    '''
    async def retrieve(self, query: str, sys: str):
        """
        """
        es_answers_dicts = await self.es_search(query, sys)
        # es_answers = asyncio.run(self.es_search(query, sys))
        
        if not es_answers_dicts: return None

        qa_pairs = [(query, answer_dict["text"]) for answer_dict in es_answers_dicts]
        scores = self.dense(qa_pairs) # все пары
        top_results = sorted(list(zip(es_answers_dicts, scores)), key=lambda x: x[1], reverse=True)[:self.parameters.llm_candidates_quantity]
        
        print("scores:", [sc for d, sc in top_results if sc >= self.parameters.ds_rank_score])

        return [d for d, sc in top_results if sc >= self.parameters.ds_rank_score]

    def __call__(self, query, sys):
        return self.retrieve(query, sys)'''
    
if __name__ == "__main__":
    import asyncio

    settings = Settings()
    parameters = Parameters()

    retriever = Retriever(settings, parameters)
    
    es_res = asyncio.run(retriever.es_search("претензии навигатор по образцам В навигаторе – сервис, который поможет подобрать подходящую для вашей ситуации претензию", 
                                             "bss"))
    for n, d in enumerate(es_res):
        print(n, "mod_id:", d["mod_id"], "doc_id:", d["doc_id"], "\n", "pub_aliases:", d["pub_aliases"], "\n\n")
    
    print(len(es_res))
    
    '''
    res = asyncio.run(retriever("Как перевести сотрудника с уменьшением оклада", "uss"))
    # res = retriever("как ответить на требование", "bss")
    print(res)'''

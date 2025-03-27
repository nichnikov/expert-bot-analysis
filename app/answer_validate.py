import os
import re
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

import asyncio
import pandas as pd
from app.dependencies import retriever, parameters
from utils.utils import jaccard_similarity


robo_chats_df = pd.read_feather(os.path.join("data", "chats_20250201_20250320", "bss_user_robo_phrases_20250201_20250320.feather"))
print(robo_chats_df)

robo_chats_dicts = robo_chats_df.to_dict(orient="records")
print(robo_chats_dicts[:5])


algorithms_type = ["Kosgu", "DenseRankerAI", "Jaccard", "SbertT5", "TFIDF", "Sbert", "DenseRankerAIClassifier"]

validate_chats = []
loop = asyncio.get_event_loop()

jcc_sim_coeff = 0.8
for d in robo_chats_dicts:
    if d["Autor"] == "MLRoboChatMessage":
        temp_d = {"chat_id": d["chat_id"], "help": d["Help"], "mod_doc": [], "title": []}
        if jaccard_similarity(d["Phrase"], "Рады приветствовать Вас на нашем сайте!") > jcc_sim_coeff:
            temp_d["Type"] = "Приветствие"
            temp_d["Algorithm"] = "Jaccard"
        
        elif jaccard_similarity(d["Phrase"], "Спасибо, что доверяете нам! Возвращайтесь с новыми вопросами.") > jcc_sim_coeff:
            temp_d["Type"] = "Прощание"
            temp_d["Algorithm"] = "Jaccard"
        
        elif jaccard_similarity(d["Phrase"], "Тест пройден") > jcc_sim_coeff:
            temp_d["Type"] = "Тест"
            temp_d["Algorithm"] = "Jaccard"

        elif jaccard_similarity(d["Phrase"], "Успешно!") > jcc_sim_coeff:
            temp_d["Type"] = "Тест"
            temp_d["Algorithm"] = "Jaccard"
        
        elif d["Autor"] == "MLRoboChatMessage":
            temp_d["Type"] = "Вопрос"
            es_get_log_query = {"match_phrase": {parameters.es_first_field: d["chat_id"]}}
            es_res = loop.run_until_complete(retriever.es_search(parameters.es_index, es_get_log_query))
            temp_d["Algorithm"] = [es_d["response"]["algorithm"] for es_d in es_res]
            for es_d in es_res:
                robo_answer = es_d["response"]["templateText"]
                docs_prm =  re.findall(r"\d{2,}", robo_answer)
                if docs_prm:
                    temp_d["mod_doc"].append(docs_prm[-2:])

        validate_chats.append(temp_d)

for d in validate_chats:
    if d["Type"] == "Вопрос":
        for m_d in d["mod_doc"]:
            mod_id = m_d[0]
            doc_id = m_d[1]
            es_query = {"bool": {"must": [{"match_phrase": {"mod_id": mod_id}},
                                        {"match_phrase": {"doc_id": doc_id}}]}}
            es_res = loop.run_until_complete(retriever.es_search("ch_documents", es_query))
            for e_d in es_res:
                d["title"].append(e_d["title"])
                    # print("title:", e_d["title"])
                    # print("text:\n", e_d["text"])
    
    
    
# Закрытие цикла событий, если он был создан вручную
if loop.is_running():
    loop.close()

validate_chats_df = pd.DataFrame(validate_chats)
print(validate_chats_df)
validate_chats_df.to_excel(os.path.join("data", "chats_20250201_20250320", "bss_robo_phrases_analysis.xlsx"), index=False)
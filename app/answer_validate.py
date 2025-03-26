import os
import re
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

import asyncio
import pandas as pd
from app.dependencies import retriever, parameters



robo_chats_df = pd.read_feather(os.path.join("data", "chats_20250201_20250320", "bss_user_robo_phrases_20250201_20250320.feather"))
print(robo_chats_df)

robo_chats_dicts = robo_chats_df.to_dict(orient="records")
print(robo_chats_dicts[:5])


algorithms_type = ["Kosgu", "DenseRankerAI", "Jaccard", "SbertT5", "TFIDF", "Sbert", "DenseRankerAIClassifier"]

validate_chats = []
loop = asyncio.get_event_loop()
for d in robo_chats_dicts[:15]:
    es_query1 = {"match_phrase": {parameters.es_first_field: d["chat_id"]}}
    es_res = loop.run_until_complete(retriever.es_search(parameters.es_index, es_query1))
    print(d["chat_id"])
    for es_d in es_res:
        answer = es_d["response"]["templateText"]
        print("algorithm:", es_d["response"]["algorithm"])
        print("templateText:", es_d["response"]["templateText"])
        print("etalon_text:", es_d["response"]["etalon_text"])
        
        docs_prm =  re.findall(r"\d{2,}", answer)
        if docs_prm:
            mod_id = docs_prm[0]
            doc_id = docs_prm[1]
            print("mod_id:", mod_id)
            print("doc_id:", doc_id)

            es_query2 = {"bool": {"must": [{"match_phrase": {"mod_id": mod_id}},
                                           {"match_phrase": {"doc_id": doc_id}}]}}

            es_res2 = loop.run_until_complete(retriever.es_search("ch_documents", es_query2))

            for d in es_res2:
                print("title:", d["title"])
                print("text:\n", d["text"])
            # print("es_res2:", es_res2)

# Закрытие цикла событий, если он был создан вручную
if loop.is_running():
    loop.close()
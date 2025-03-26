import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

import asyncio
import pandas as pd
from app.dependencies import retriever



robo_chats_df = pd.read_feather(os.path.join("data", "chats_20250201_20250320", "bss_user_robo_phrases_20250201_20250320.feather"))
print(robo_chats_df)

robo_chats_dicts = robo_chats_df.to_dict(orient="records")
print(robo_chats_dicts[:5])


validate_chats = []
loop = asyncio.get_event_loop()
for d in robo_chats_dicts[:15]:
    es_res = loop.run_until_complete(retriever.es_search(d["chat_id"]))
    print(d["chat_id"])
    for es_d in es_res:
        print("Phrase:", d["Phrase"])
        print("algorithm:", es_d["response"]["algorithm"])
        print("templateText:", es_d["response"]["templateText"])
        print("etalon_text:", es_d["response"]["etalon_text"], "\n\n")

# Закрытие цикла событий, если он был создан вручную
if loop.is_running():
    loop.close()
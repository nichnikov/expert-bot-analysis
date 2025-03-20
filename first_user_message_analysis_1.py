"""
Выбирает из каждого чата первое сообщение пользователя и сохраняет
"""
import os
import pandas as pd
from services.data_processor import ChatDataProcessor


data_path = os.path.join("data", "first_user_message_analysis", "bss_chats_20250201_20250320.feather")
df = pd.read_feather(data_path)
print(df)

processor = ChatDataProcessor(data_path)
processor.pipline()

k = 1
first_user_messages = []
for i in processor.dict_of_chats:
    for d in processor.dict_of_chats[i]:
        if d["Autor"] == "Пользователь":
            len_w = len(d["Phrase"].split())
            first_user_messages.append({"chat_id": i,
                                        "FirstPhrase": d["Phrase"],
                                        "len_w": len_w})
            if len_w > 3:
                break

    if k > 2000000:
        break
    k += 1

first_user_messages_df = pd.DataFrame(first_user_messages)
print(first_user_messages_df)
out_path = os.path.join("data", "first_user_message_analysis", "bss_user_first_phrase_20250201_20250320_3_and_more.feather")
first_user_messages_df.to_feather(out_path)
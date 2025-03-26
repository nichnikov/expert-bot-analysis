"""
Выбирает из каждого чата, в котором робот ответил пользователю первое сообщение пользователя (и ответ робота) и сохраняет
"""
import os
import pandas as pd
from services.data_processor import ChatDataProcessor


data_path = os.path.join("data", "chats_20250201_20250320", "bss_chats_20250201_20250320.feather")
df = pd.read_feather(data_path)
print(df)

processor = ChatDataProcessor(data_path)
processor.pipline(**{"aggregation": False})


k = 1
robo_user_messages = []
for i in processor.dict_of_chats:
    phrase_chain = processor.dict_of_chats[i]
    discriminators = [d["Autor"] for d in phrase_chain]
    if "UserMessage" and "MLRoboChatMessage" in discriminators:
        temp_phrase = []
        for d in phrase_chain:
            if d["Autor"] == "MLRoboChatMessage":
                temp_phrase = phrase_chain[:phrase_chain.index(d)+1]
                if "OperatorMessage" not in discriminators: 
                    chat_type = "helped" 
                else: chat_type = "not_helped"
        robo_user_messages += [{"chat_id": i, 
                            "Phrase": d["Phrase"],
                            "Autor": d["Autor"],
                            "Help": chat_type
                                } for d in temp_phrase if d["Autor"] in ["UserMessage", "MLRoboChatMessage"]]

    if k > 5000000:
        break
    k += 1

robo_user_messages_df = pd.DataFrame(robo_user_messages)
robo_user_messages_df["len_w"] = robo_user_messages_df["Phrase"].apply(lambda x: len(x.split()))

print(robo_user_messages_df)

out_path = os.path.join("data", "chats_20250201_20250320", "bss_user_robo_phrases_20250201_20250320.feather")
robo_user_messages_df.to_feather(out_path)

out_path_xlsx = os.path.join("data", "chats_20250201_20250320", "bss_user_robo_phrases_20250201_20250320.xlsx")
robo_user_messages_df.to_excel(out_path_xlsx, index=False)


'''
first_user_messages_df = pd.DataFrame(first_user_messages)
print(first_user_messages_df)
out_path = os.path.join("data", "first_user_message_analysis", "bss_user_first_phrase_20250201_20250320_3_and_more.feather")
first_user_messages_df.to_feather(out_path)'''
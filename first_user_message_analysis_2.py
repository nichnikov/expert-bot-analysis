"""
Распределение чатов по длине входящего вопроса пользователя (количество чатов / длина входящего вопроса)
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

# data_path = os.path.join("data", "first_user_message_analysis", "bss_user_first_phrase_20250201_20250320.feather")
data_path = os.path.join("data", "first_user_message_analysis", "bss_user_first_phrase_20250201_20250320_3_and_more.feather")
df = pd.read_feather(data_path)

mss_by_len = df[["chat_id", "len_w"]].groupby("len_w", as_index=False).count()
'''
print(df)
data_out = os.path.join("data", "first_user_message_analysis", "bss_user_first_phrase_20250201_20250320_3_and_more.xlsx")
df.to_excel(data_out, index=False)'''

print(mss_by_len)

fig, ax = plt.subplots()
ax.bar(mss_by_len["len_w"], mss_by_len["chat_id"])


ax.set_xlabel('длина первого сообщения')
ax.set_ylabel('количество чатов')
ax.set_title('Количество чатов в зависимости от длины первого сообщения')

plt.show()

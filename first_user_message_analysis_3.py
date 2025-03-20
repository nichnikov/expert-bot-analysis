import os
import re
import pandas as pd
from core.data_definition import Parameters, Settings
from services.validator import GPT_Validator

settings = Settings()
parameters = Parameters()
parameters.prompt = """
        Выбери из списка, чем является сообщение от пользователя. 
        Возвращай только элементы списка.
            Список:
            1. Приветствие
            2. Бухгалтерский или юридический вопрос
            3. Вопрос в техподдержку
            4. Благодарность
            5. Другое

        Вопрос пользователя: {}
"""

# поля в данных:
'''
    "FirstPhrase"
    "chat_id"
    "len_w"'''

validator = GPT_Validator(settings, parameters)
data_path = os.path.join("data", "first_user_message_analysis", "bss_user_first_phrase_20250201_20250320_3_and_more.feather")
data_df = pd.read_feather(data_path)
data_dicts = data_df.to_dict(orient="records")
k = 1
for d in data_dicts:
    phrase = d["FirstPhrase"]
    val = validator.gpt_validation(phrase)
    answer_num = re.findall("[12345]", val)
    
    print(k, phrase, "\n", val, "\n", answer_num, "\n\n" )
    

    k += 1
    if k > 100:
        break
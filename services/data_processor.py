import os
import re
import sys
import json
import logging
import pandas as pd
from collections import namedtuple
from itertools import groupby
from operator import itemgetter

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.utils import chunks

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')




# Класс для обработки данных чата
class ChatDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_df = None
        self.tuples_of_chats = []
        self.dict_of_chats = {}

    def load_data(self):
        """Загружает данные из файла, поддерживает feather и csv форматы."""
        file_extension = os.path.splitext(self.file_path)[1]
        
        assert file_extension in [".csv", ".feather"]
        
        if file_extension == '.feather':
            self.data_df = pd.read_feather(self.file_path)
            logging.info(f"Данные загружены из Feather файла: {self.file_path}")
        elif file_extension == '.csv':
            self.data_df = pd.read_csv(self.file_path, sep="\t")
            logging.info(f"Данные загружены из CSV файла: {self.file_path}")
        else:
            logging.error("Формат файла не поддерживается. Поддерживаются только .feather и .csv форматы.")
            raise ValueError("Формат файла не поддерживается. Поддерживаются только .feather и .csv форматы.")
        self._clean_columns()

    def _clean_columns(self):
        """Очищает названия колонок и содержимое от нежелательных символов."""
        for cl in self.data_df.columns:
            clear_cn = re.sub(r"\s+", "", cl)
            self.data_df.rename(columns={cl: clear_cn}, inplace=True)

        patterns = re.compile(r"\n|\¶|(?P<url>https?://[^\s]+)|<a href=|</a>|/#/document/\d\d/\d+/|\"\s*\">|\s+")
        for col in ["chat_id", "text"]:
            self.data_df[col] = self.data_df[col].apply(lambda x: patterns.sub(" ", str(x)))

        self.data_df["created"] = pd.to_datetime(self.data_df["created"])
        logging.info("Колонки данных очищены и обновлены.")

    def classify_authors(self):
        """Классифицирует авторов сообщений."""
        user_messages = [
            "UserMessage", "UserNewsPositiveReactionMessage", 
            "UserMobileMessage", "UserFileMessage"
        ]
        operator_messages = [
            "AutoGoodbyeMessage", "AutoHello2Message",  "AutoHelloMessage", 
            "AutoHelloNewsMessage", "AutoHelloOfflineMessage", "AutoRateMessage", 
            "HotlineNotificationMessage", "MLRoboChatMessage", "NewsAutoMessage", 
            "OperatorMessage"
        ]

        self.data_df["Autor"] = "Нет"
        self.data_df["Autor"][self.data_df["discriminator"].isin(user_messages)] = "Пользователь"
        self.data_df["Autor"][self.data_df["discriminator"].isin(operator_messages)] = "Оператор"
        logging.info("Авторы сообщений классифицированы.")

    def group_messages(self):
        """Группирует сообщения по chat_id."""
        data_dics = self.data_df[["chat_id", "created", "Autor", "text"]].to_dict(orient="records")
        Phrase = namedtuple("Phrase", ["ChatID", "Autor", "Phrase", "Timestamp"])
        data_dics.sort(key=itemgetter('chat_id'))
        dict_of_chats = {int(k): sorted([Phrase(k, d["Autor"], d["text"], d["created"]) for d in list(g)], key=lambda x: x.Timestamp)
                               for k, g in groupby(data_dics, itemgetter("chat_id"))}
        for i in dict_of_chats:
            self.tuples_of_chats += dict_of_chats[i]
        for i in dict_of_chats:
            self.dict_of_chats[i] = [{"Autor": nt.Autor, "Phrase": nt.Phrase} for nt in dict_of_chats[i]]
        logging.info("Сообщения сгруппированы по chat_id.")

    def save_grouped_data_table(self, out_dir, how="csv"):
        """Сохраняет сгруппированые данные в JSON."""
        assert how in ["csv", "xlsx"]
        grouped_chats_df = pd.DataFrame(self.tuples_of_chats)
        
        if how == "csv":
            out_path_df = os.path.join(out_dir, "grouped_chats.csv")
            grouped_chats_df.to_csv(out_path_df, sep="\t", index=False)
        else:
            out_path_df = os.path.join(out_dir, "grouped_chats.xlsx")
            grouped_chats_df.drop("Timestamp", axis=1).to_excel(out_path_df, index=False)
    
    def save_grouped_data_jsons(self, out_dir, chank_size):
        keys = self.dict_of_chats.keys()
        keys_chunks = chunks(list(keys), chank_size)
        
        for num, keys_chank in enumerate(keys_chunks):
            fn = "grouped_chats" + str(num) + ".json"
            out_path_json = os.path.join(out_dir, fn)
            temp_dict = {i: self.dict_of_chats[i] for i in keys_chank}
            with open(out_path_json, "w") as f:
                json.dump(temp_dict, f, ensure_ascii=False)
                logging.info(f"Группированные данные сохранены в {out_path_json}.")
    
    def pipline(self, what="save", **kwads):
        self.load_data()
        self.classify_authors()
        self.group_messages()



# Пример использования класса
if __name__ == "__main__":
    processor = ChatDataProcessor(os.path.join("data", "test_data.csv"))
    processor.load_data()
    processor.classify_authors()
    processor.group_messages()
    processor.save_grouped_data_jsons(os.path.join("data", "jsons"), 100)

    k = 1
    for i in processor.dict_of_chats:
        print(processor.dict_of_chats[i])
        if k > 5:
            break
        k += 1
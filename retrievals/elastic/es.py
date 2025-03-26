# бесчеловечный код
import sys
import os
from typing import Any, List
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_bulk

# Установка пути для поиска модулей
current_file_path = os.path.abspath(__file__)
print("current_file_path:", current_file_path)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
sys.path.append(project_root)
# sys.path.append("/home/an/data/github/AITK611-expert-bot-service-with-baai-openai")
# sys.path.append("/home/an/Data/github/AITK611-expert-bot-service-with-baai-openai")

from core.data_types import Settings, Parameters
from core.config import logger


class ElasticClient:
    """Клиент для работы с Elasticsearch."""

    def __init__(self, settings: Settings, parametrs: Parameters):
        self.parametrs = parametrs
        self.settings = settings
        self.client = AsyncElasticsearch(
            hosts=self.settings.es_hosts,
            basic_auth=(self.settings.es_login, self.settings.es_password),
            request_timeout=self.parametrs.es_request_timeout,
            max_retries=self.parametrs.es_max_retries,
            retry_on_timeout=self.parametrs.es_retry_on_timeout,
        )
        self.chunk_size = self.parametrs.es_chunk_size
        self.max_hits = self.parametrs.es_max_hits

    async def create_index(self, index_name: str) -> None:
        """Создает индекс, если он не существует."""
        try:
            await self.client.indices.create(index=index_name)
            logger.info(f"Индекс {index_name} успешно создан.")
        except Exception as e:
            logger.error(f"Не удалось создать индекс {index_name}: {e}")

    async def delete_index(self, index_name: str) -> None:
        """Удаляет индекс, если он существует."""
        try:
            await self.client.indices.delete(index=index_name)
            logger.info(f"Индекс {index_name} успешно удален.")
        except NotFoundError:
            logger.warning(f"Индекс {index_name} не существует.")
        except Exception as e:
            logger.error(f"Не удалось удалить индекс {index_name}: {e}")

    async def search_query(self, index: str, query: dict) -> Any:
        """Выполняет поиск по заданному индексу и запросу."""
        try:
            response = await self.client.search(
                index=index,
                query=query,
                size=self.max_hits,
                allow_partial_search_results=True,
                min_score=0,
            )
            logger.info(f"Поиск в индексе {index} выполнен успешно.")
            return response
        except Exception as e:
            logger.error(f"Ошибка при выполнении поиска в индексе {index}: {e}")
            return None

    async def add_docs(self, index_name: str, docs: List[dict]) -> None:
        """Добавляет документы в указанный индекс."""
        try:
            actions = ({"_index": index_name, "_source": doc} for doc in docs)
            success, _ = await async_bulk(
                self.client, actions, chunk_size=self.chunk_size
            )
            logger.info(f"Добавлено {success} документов в индекс {index_name}.")
        except Exception as e:
            logger.error(f"Ошибка при добавлении документов в индекс {index_name}: {e}")

    async def close(self) -> None:
        """Закрывает соединение с Elasticsearch."""
        await self.client.close()
        logger.info("Соединение с Elasticsearch закрыто.")

# Пример использования
async def main():
    # Загрузка настроек
    settings = Settings()
    parameters = Parameters()

    # Создание клиента
    es_client = ElasticClient(settings, parameters)

    # Работа с Elasticsearch
    # await es_client.create_index("test_index")
    # await es_client.add_docs("test_index", [{"name": "doc1"}, {"name": "doc2"}])
    
    query =  {"bool": 
              {"must": [{"match" : {"text_lem": "Как ответить на требование"}}, {"match_phrase": {"pub_aliases": "uss"}}]}}
    # response = await es_client.search_query("publicator_paragraphs*", {"match_all": {}})
    response = await es_client.search_query("publicator_paragraphs*", query)
    for i in response:
        print(i)
    
    print(len(response["hits"]["hits"]))
    print(response["hits"]["hits"][:5])

    # Закрытие соединения
    await es_client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

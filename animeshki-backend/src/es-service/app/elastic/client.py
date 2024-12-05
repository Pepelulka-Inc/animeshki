import asyncio
import logging
from typing import List, Dict

from elasticsearch import AsyncElasticsearch
from aiohttp.web import Application


logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


# класс для работы с эластиком
class ElasticClient:
    _instance = None

    def __new__(cls, url: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, url: str):
        if not self._initialized:
            self.client = AsyncElasticsearch(url)
            self._initialized = True

# часть инициализации elasricsearch
    async def run(self, app: Application):
        asyncio.create_task(self.create_main_index())

    async def stop(self, app: Application):
        await self.client.close()

# создание основного индекса в эластике, в котором будет производиться поиск
# в нём хранится название аниме и его id из БД, изначально пустой
    async def create_main_index(self):
        index_name = "anime"
        config = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "russian_english_analyzer": {
                            "tokenizer": "standard",
                            "filter": ["lowercase", "russian_stemmer", "english_stemmer"]
                        }
                    },
                    "filter": {
                        "russian_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "russian_english_analyzer"},
                    "id": {"type": "keyword", "index": False},
                }
            }
        }
        try:
            await self.client.indices.create(index=index_name, body=config)
        except Exception as e:
            logger.error(f"Failed to create index: {e}")

# непосредственно поиск аниме в индексе, метод используется только ручкой
    async def search(self, search_query: str) -> List[Dict[str, float]]:
        query = {"query": {"match": {"title": search_query}}}
        try:
            es_response = await self.client.search(index="anime", body=query)
        except Exception as e:
            logger.error(f"Failed to search anime: {e}")
        hits = es_response["hits"]["hits"]
        response = []
        for hit in hits:
            response.append({"id": hit["_id"], "score": hit["_score"]})
        return response

# добавление некоторого количества анимешек, если того потребует какой-то другой сервис, с которым мой общается через кафку
    async def add(self, anime_list: list):
        if len(anime_list) == 1:
            document = anime_list[0]
            try:
                await self.client.index(index="anime", id=document["id"], document=document)
            except Exception as e:
                logger.error(f"Failed to add anime in index: {e}")
        else:
            query = []
            for i in range(len(anime_list)):
                query.append({"index": {"_index": "anime", "_id": anime_list[i]["id"]}})
                query.append(anime_list[i])
            try:
                await self.client.bulk(body=query)
            except Exception as e:
                logger.error(f"Failed to add anime in index: {e}")

# удаление некоторого количества анимешек
    async def delete(self, id_list: list):
        if len(id_list) == 1:
            try:
                await self.client.delete(index="anime", id=id_list[0])
            except Exception as e:
                logger.error(f"Failed to delete anime from index: {e}")
        else:
            query = []
            for i in range(id_list.len()):
                query.append({"delete": {"_index": "anime", "_id": id_list[i]}})
            try:
                await self.client.bulk(body=query)
            except Exception as e:
                logger.error(f"Failed to delete anime from index: {e}")
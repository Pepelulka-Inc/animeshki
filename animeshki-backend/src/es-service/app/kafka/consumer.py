import json
import logging
import asyncio

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from confluent_kafka.admin import AdminClient, NewTopic
from aiohttp.web import Application

from settings import KAFKA_TOPIC
from elastic import get_elastic_client


logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


# класс для работы с кафкой
class KafkaConsumer:
    _instance = None

    def __new__(cls, bootstrap_server: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, bootstrap_server: str):
        if not self._initialized:
            self.bootstrap_server = bootstrap_server
            self.create_topic()
            self.consumer = None
            self._initialized = True

    # создание топика, через который происходит общение с другим сервисом
    def create_topic(self):
        admin_client = AdminClient({"bootstrap.servers": self.bootstrap_server})
        topic_list = [
            NewTopic(topic=KAFKA_TOPIC, num_partitions=1, replication_factor=1)
        ]
        try:
            admin_client.create_topics(topic_list)
        except Exception as e:
            logger.error(f"Failed to create topic: {e}")

    # часть инициализации кафки
    async def run(self, app: Application):
        asyncio.create_task(self.consume())

    async def stop(self, app: Application):
        await self.consumer.stop()

    # обработка сообщений, приходящих с топика
    # в теле сообщения должно быть только 2 поля: action и body
    # всего 2 вида action: add и delete
    # в body всегда хранится список, наполнение которого зависит от action
    # если action = delete, в списке просто хранятся id аниме, которые нужно удалить
    # если action = add, список состоит из пар title и id
    async def consume(self):
        self.consumer = AIOKafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=self.bootstrap_server,
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        async for msg in self.consumer:
            await self.process_kafka_msg(msg)

    async def process_kafka_msg(self, msg: ConsumerRecord):
        es_client = get_elastic_client()
        msg_body = json.loads(msg.value.decode("utf-8"))
        if msg_body["action"] == "add":
            await es_client.add(anime_list=msg_body["body"])
        elif msg_body["action"] == "delete":
            await es_client.delete(id_list=msg_body["body"])

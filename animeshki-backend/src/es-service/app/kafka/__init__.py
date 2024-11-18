from kafka.consumer import KafkaConsumer
from settings import KAFKA_BOOTSTRAP_SERVER


def get_kafka_consumer() -> KafkaConsumer:
    return KafkaConsumer(KAFKA_BOOTSTRAP_SERVER)

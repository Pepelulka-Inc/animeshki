import os

ES_URL: str = os.getenv("ES_URL", "http://elasticsearch:9200")

KAFKA_BOOTSTRAP_SERVER: str = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")
KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "es-topic")

SERVICE_PORT: int = 8001
SERVICE_HOST: str = "0.0.0.0"
HANDLER_ENDPOINT: str = "/search"
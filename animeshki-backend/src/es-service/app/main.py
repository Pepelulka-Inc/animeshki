from aiohttp.web import Application, run_app

from elastic import get_elastic_client
from kafka import get_kafka_consumer
from settings import HANDLER_ENDPOINT, SERVICE_PORT, SERVICE_HOST
from handlers import search_anime


# при перед стартом приложения инициализируются все необходимые сервисы
# при завершении все клиенты сервисов закрываются
def create_app() -> Application:
    es_client = get_elastic_client()
    kafka_consumer = get_kafka_consumer()
    app = Application()
    app.router.add_get(path=HANDLER_ENDPOINT, handler=search_anime)
    app.on_startup.append(es_client.run)
    app.on_startup.append(kafka_consumer.run)
    app.on_cleanup.append(kafka_consumer.stop)
    app.on_cleanup.append(es_client.stop)
    return app


if __name__ == "__main__":
    app = create_app()
    run_app(app, host=SERVICE_HOST, port=SERVICE_PORT)

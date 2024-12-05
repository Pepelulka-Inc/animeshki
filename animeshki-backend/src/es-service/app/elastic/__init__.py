from elastic.client import ElasticClient
from settings import ES_URL


def get_elastic_client() -> ElasticClient:
    return ElasticClient(ES_URL)

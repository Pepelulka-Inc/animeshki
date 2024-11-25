import os
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger("minio-service.settings")

# Настройки сервиса
IS_INIT_MODE_ON: bool = os.getenv("MINIO_SERVICE_INIT_MODE") == "1"
PORT: int = 8000

# Настройки MINIO
MINIO_SETTINGS: Dict[str, str] = {
    "endpoint": "http://minio:9000",
    "username": os.getenv("MINIO_SERVICE_USER_NAME"),
    "password": os.getenv("MINIO_SERVICE_USER_PASSWORD"),
    "bucket": os.getenv("MINIO_SERVICE_BUCKET_NAME"),
}

# Проверка обязательных переменных окружения:

_REQUIRED_ENV_VARS: List[str] = [
    MINIO_SETTINGS["username"],
    MINIO_SETTINGS["password"],
    MINIO_SETTINGS["bucket"],
]


def _check_env_vars():
    for env_var in _REQUIRED_ENV_VARS:
        if env_var == "":
            logger.fatal(f"Env var {env_var} is not defined")
            exit(1)


_check_env_vars()

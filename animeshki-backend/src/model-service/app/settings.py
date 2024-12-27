import os
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger("minio-service.settings")

USE_MINIO: bool = True if os.getenv("USE_MINIO", False) == "True" else False
DEBUG: bool = True if os.getenv("DEBUG", False) == "True" else False
# Настройки сервиса
PORT: int = 8000

# Настройки MINIO
MODEL_SETTINGS: Dict[str, str] = {
    "EPOCHS": os.getenv("MODEL_TRAIN_EPOCHS", 100),
    "NO_COMPONENTS": os.getenv("MODEL_TRAIN_NO_COMPONENTS", 10),
    "NUM_THREADS": os.getenv("MODEL_TRAIN_NUM_THREADS", 12),
    "FILENAME": os.getenv("MODEL_TRAIN_FILENAME", "rec_anime_model.h5"),
}

# Проверка обязательных переменных окружения:

_REQUIRED_ENV_VARS: List[str] = [
    MODEL_SETTINGS["EPOCHS"],
    MODEL_SETTINGS["NO_COMPONENTS"],
    MODEL_SETTINGS["FILENAME"],
    MODEL_SETTINGS["NUM_THREADS"]
]


def _check_env_vars():
    for env_var in _REQUIRED_ENV_VARS:
        if env_var == "":
            logger.fatal(f"Env var {env_var} is not defined")
            exit(1)


_check_env_vars()
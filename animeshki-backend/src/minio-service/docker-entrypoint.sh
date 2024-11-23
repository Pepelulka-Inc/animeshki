#!/bin/bash
# Скрипт сделан для изначальной инициализации minio (чтобы не надо было делать этого вручную)

# Скрипт работает только если MINIO_SERVICE_INIT_MODE=1
if [[ "${MINIO_SERVICE_INIT_MODE}" == "1" ]]; then
  echo "[info] minio-service init.sh: init mode on"
  # Проверяем установлены ли нужные переменные окружения
  if [ -z "${MINIO_ROOT_USER}" ]; then
    echo "[fatal] minio-service init.sh: MINIO_ROOT_USER env var is empty"
    exit 1
  fi

  if [ -z "${MINIO_ROOT_PASSWORD}" ]; then
    echo "[fatal] minio-service init.sh: MINIO_ROOT_PASSWORD env var is empty"
    exit 1
  fi

  # Подождем пока minio проснется
  sleep 3

  # Подключаемся к minio
  mc alias set my_minio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
  # Создаем пользователя
  mc admin user add my_minio ${MINIO_SERVICE_USER_NAME} ${MINIO_SERVICE_USER_PASSWORD}
  # Устанавливаем пользователю права на чтение и запись файлов
  mc admin policy attach my_minio readwrite --user=${MINIO_SERVICE_USER_NAME}
  # Создаем бакет
  mc mb my_minio/${MINIO_SERVICE_BUCKET_NAME}

else
  echo "minio-service init.sh: init mode off"
fi

# Запускаем основное приложение
$@

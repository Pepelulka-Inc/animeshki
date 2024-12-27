FROM python:3.10-slim

WORKDIR /root/

# Для режима начальной инициализации: (смотреть README.md)
# Установка mc (minio client)
RUN apt-get update

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY ./docker-entrypoint.sh ./app/docker-entrypoint.sh

WORKDIR /root/app

CMD ["python", "main.py", $PORT]

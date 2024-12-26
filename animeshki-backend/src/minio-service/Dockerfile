FROM python:3.10-slim

WORKDIR /root/

# Для режима начальной инициализации: (смотреть README.md)
# Установка mc (minio client)
RUN apt-get update
RUN apt install -y curl dos2unix
COPY ./bin/mc ./mc
RUN chmod +x ./mc
RUN mv ./mc /usr/bin

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY ./docker-entrypoint.sh ./app/docker-entrypoint.sh

EXPOSE 8000

WORKDIR /root/app

RUN dos2unix docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "main.py"]

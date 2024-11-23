FROM python:3.10-slim

WORKDIR /root/

# Для режима начальной инициализации: (смотреть README.md)
# Установка mc (minio client)
RUN apt-get update
RUN apt install -y curl
RUN curl https://dl.min.io/client/mc/release/linux-amd64/mc -o ./mc
RUN chmod +x ./mc
RUN mv ./mc /usr/bin

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
RUN mv ./docker-entrypoint.sh ./app

EXPOSE 8000

WORKDIR /root/app

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "main.py"]

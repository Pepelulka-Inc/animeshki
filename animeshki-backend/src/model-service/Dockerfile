FROM python:3.10-slim
ENV MODEL_PORT 8000
WORKDIR /root/
# Для режима начальной инициализации: (смотреть README.md)
RUN apt-get update
# COPY ./bin ./bin
COPY requirements.txt .
RUN apt install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

WORKDIR /root
EXPOSE ${MODEL_PORT}

CMD ["python", "app/main.py"]

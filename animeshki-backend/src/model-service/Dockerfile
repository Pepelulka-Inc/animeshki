FROM python:3.10-slim

WORKDIR /root/
ARG PORT=8000
# Для режима начальной инициализации: (смотреть README.md)
RUN apt-get update

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

WORKDIR /root/app

EXPOSE ${PORT}

CMD ["python", "main.py"]

FROM python:3.11-slim

WORKDIR /root/

RUN apt-get update

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

WORKDIR /root/app

CMD ["python", "main.py"]
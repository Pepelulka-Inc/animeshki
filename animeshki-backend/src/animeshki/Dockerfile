FROM python:3.10-slim

WORKDIR /root/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app.py __init__.py ./
COPY ./infrastructure ./infrastructure
COPY ./domain ./domain
COPY ./api ./api

ENTRYPOINT ["python"]
CMD ["app.py"]

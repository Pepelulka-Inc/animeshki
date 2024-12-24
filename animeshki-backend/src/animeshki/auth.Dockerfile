FROM python:3.10-slim

WORKDIR /root/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Так как auth требуется infrastructure запихиваем ее тоже выборочно
COPY ./auth.py ./__init__.py ./
COPY ./infrastructure ./infrastructure

ENTRYPOINT ["python"]
CMD ["auth.py"]

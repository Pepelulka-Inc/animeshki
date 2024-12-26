import logging
from asyncio import StreamReader
from typing import AsyncGenerator, List, Dict

import aioboto3

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger("minio-service.connection")


# Этот класс - обертка над открытым подключением к S3 хранилищу
# Он возвращается при `async with connection as client`, где connection - экземпляр S3Connection
class S3Client:
    def __init__(self, s3_opened_connection):
        self.s3_client = s3_opened_connection

    # Возвращаем генератор
    async def get_file_stream(self, bucket: str, filename: str) -> AsyncGenerator:
        response_from_s3 = await self.s3_client.get_object(Bucket=bucket, Key=filename)
        async for chunk in response_from_s3["Body"].iter_chunks():
            yield chunk

    # in_stream должен иметь метод read(n)
    async def upload_file_from_stream(self, in_stream, bucket: str, filename: str):
        await self.s3_client.upload_fileobj(in_stream, bucket, filename)

    async def get_file_list(self, bucket: str) -> List[Dict[str, str]]:
        response = await self.s3_client.list_objects_v2(Bucket=bucket)
        files = response.get("Contents", [])

        # Format the output
        file_list = [
            {
                "Key": file["Key"],
                "Size": file["Size"],
                "LastModified": file["LastModified"].isoformat(),
            }
            for file in files
        ]

        return file_list


# Класс контекстный менеджер. Возвращает S3Client
class S3Connection:
    def __init__(self, url: str, access_key: str, secret_key: str):
        self.access_key: str = access_key
        self.secret_key: str = secret_key
        self.url: str = url

    async def __aenter__(self) -> S3Client:
        self.session: aioboto3.Session = aioboto3.Session()
        self.s3_client_ctx_manager = self.session.client(
            "s3",
            endpoint_url=self.url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="us-east-1",
        )
        opened_client = await self.s3_client_ctx_manager.__aenter__()
        self.client = S3Client(opened_client)
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.s3_client_ctx_manager.__aexit__(exc_type, exc_val, exc_tb)

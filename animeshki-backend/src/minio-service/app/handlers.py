import logging

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response, StreamResponse

from file_manager import File

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger("minio-service.handlers")


# Ручка для просмотра списка всех файлов
async def get_files_list(request: Request) -> Response:
    try:
        async with request.app["s3_connection"] as client:
            result = await client.get_file_list(request.app["s3_bucket"])
        return web.json_response(data=result)
    except Exception as e:
        logger.error(f"Failed to get files list: {e}")
        return web.json_response(status=500, data=[])


# Хендлеру нужен path parameter 'filename'
# Ручка для скачивания файла
async def get_file(request: Request) -> StreamResponse:
    filename: str = request.match_info.get("filename")
    file: File = File(name=filename)
    file.pending_upload()
    try:
        async with request.app["s3_connection"] as client:
            stream = client.get_file_stream(request.app["s3_bucket"], filename)

            headers = {
                "Content-Disposition": f"attachment; filename={filename}",
            }

            response = StreamResponse(headers=headers)

            await response.prepare(request)

            file.in_progress()

            # Пишем содержимое файла в ответ
            async for chunk in stream:
                await response.write(chunk)

            file.loaded()
            await response.write_eof()  # Конец записи файла

            file.success()
            return response
    except Exception as e:
        logger.error(f"Failed to get file {filename}: {e}")
        file.failed()
    finally:
        return web.Response(status=404)

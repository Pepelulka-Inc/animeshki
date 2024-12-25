import logging
import os

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


# Базовая реализация обработки запроса на получение какого-то файла. Все ручки получения файлов
# реализованы через эту функцию.
async def get_file_base(request, prefix=""):
    filename: str = request.match_info.get("filename")
    filename = prefix + filename
    file: File = File(name=filename)
    file.pending_upload()
    try:
        async with request.app["s3_connection"] as client:
            stream = client.get_file_stream(request.app["s3_bucket"], filename)

            headers = {
                "Content-Disposition": f"attachment; filename={os.path.basename(filename)}"
            }

            response = StreamResponse(headers=headers)

            file.in_progress()

            # Пишем содержимое файла в ответ
            prepared_flag = False  # Ебанутый костыль для проверки того, что файл существует (про него ниже)
            async for chunk in stream:
                if not prepared_flag:
                    await response.prepare(request)
                    prepared_flag = True
                await response.write(chunk)
            # Зачем флаг prepared_flag и вся эта суета?
            # Ответ - я не знаю, как проверить успешность выполнения get_object в aioboto3, потому
            # что у него очень хреновая документация (ее почти нет).
            # Поэтому когда я в цикле перебираю вывод stream (который является асинхронным генератором)
            # он может выдать исключение, которое обработается блоком try/except и функция вернет ответ 404.
            # Если же исключения не было, я вызываю response.prepare и обрабатываю все чанки. Если вызвать
            # response.prepare перед циклом, то в случае, если файла в хранилище не было, он вернет испорченный
            # запрос.

            file.loaded()
            await response.write_eof()  # Конец записи файла

            file.success()
            return response
    except Exception as e:
        logger.error(f"Failed to get file {filename}: {e}")
        file.failed()
    return web.Response(status=404)


# Хендлеру нужен path parameter 'filename'
# Ручка для скачивания файла (для файлов в корневой директории)
async def get_file(request: Request) -> StreamResponse:
    return await get_file_base(request)


# Хендлеру нужен path parameter 'filename'
# Ручка для скачивания картинки (в директории images)
async def get_image(request: Request) -> StreamResponse:
    return await get_file_base(request, prefix="images/")


# Хендлеру нужен path parameter 'filename'
# Ручка для скачивания видео (в директории videos)
async def get_video(request: Request) -> StreamResponse:
    return await get_file_base(request, prefix="videos/")


# Базовая реализация обработки запроса на отправку какого-то файла. Все ручки отправки файлов
# реализованы через эту функцию.
async def upload_file_base(request: Request, prefix=""):
    # Чтение данных из формы (multipart)
    data = await request.post()

    file_path = data.get("file_path")
    if not file_path:
        return web.Response(status=400, text="File path is required")

    file_field = data.get("file")
    if not file_field:
        return web.Response(status=400, text="File is required")

    file_path = prefix + file_path

    try:
        async with request.app["s3_connection"] as client:
            await client.upload_file_from_stream(
                file_field.file, request.app["s3_bucket"], file_path
            )
            logger.warning("success")
        return web.json_response({"msg": "success"})
    except Exception as e:
        logger.error(f"Failed to upload file {file_path}: {e}")
    return web.Response(status=500)


# Ручка для загрузки любых файлов по любому пути
async def upload_file(request: Request) -> StreamResponse:
    return await upload_file_base(request)


# Ручка для загрузки картинок
async def upload_image(request: Request) -> StreamResponse:
    return await upload_file_base(request, prefix="images/")


# Ручка для загрузки видео
async def upload_video(request: Request) -> StreamResponse:
    return await upload_file_base(request, prefix="videos/")

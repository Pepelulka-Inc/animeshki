import asyncio

from aiohttp.web import Application, run_app

from settings import MINIO_SETTINGS, PORT
from connection import S3Connection
from handlers import (
    get_files_list,
    get_file,
    upload_file,
    get_image,
    get_video,
    upload_image,
    upload_video,
)


async def get_application() -> Application:
    app: Application = Application()
    app.router.add_get("/s3", get_files_list)
    app.router.add_get("/s3/download/{filename}", get_file)
    app.router.add_get("/s3/download/image/{filename}", get_image)
    app.router.add_get("/s3/download/video/{filename}", get_video)

    app.router.add_post("/s3/upload/any", upload_file)
    app.router.add_post("/s3/upload/image", upload_image)
    app.router.add_post("/s3/upload/video", upload_video)

    app["s3_connection"] = S3Connection(
        MINIO_SETTINGS["endpoint"],
        MINIO_SETTINGS["username"],
        MINIO_SETTINGS["password"],
    )
    app["s3_bucket"] = MINIO_SETTINGS["bucket"]

    return app


if __name__ == "__main__":
    app: Application = asyncio.run(get_application())
    run_app(app, host="0.0.0.0", port=PORT)

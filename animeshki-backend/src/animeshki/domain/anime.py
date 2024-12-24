import uuid

from pydantic import BaseModel


class AnimeModel(BaseModel):
    anime_id: str
    title: str
    description: str
    picture_minio_path: str


class AnimeCreateModel(BaseModel):
    title: str
    description: str
    picture_minio_path: str

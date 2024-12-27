from pydantic import BaseModel


class AnimeModel(BaseModel):
    anime_id: str
    title: str
    description: str
    picture_minio_path: str | None
    mal_id: int | None


class AnimeCreateModel(BaseModel):
    title: str
    description: str
    picture_minio_path: str | None
    mal_id: int | None

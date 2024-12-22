from sqlalchemy import Column, Integer, String, Uuid, ForeignKey
from sqlalchemy.orm import DeclarativeBase

__all__ = [
    "User",
    "Favorites",
    "Anime",
    "Anime_stat",
    "Anime_episode",
    "Comments",
    "UserAnimeStarsCount",
]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = "user"

    id = Column(Integer, unique=True, primary_key=True)
    username = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(128))
    role = Column(String(16))


class Favorites(Base):
    __tablename__ = "favorites"

    id = Column(Integer, unique=True, primary_key=True)
    username = Column(
        String(32), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE")
    )
    anime_id = Column(
        Uuid, ForeignKey("anime.anime_id", onupdate="CASCADE", ondelete="CASCADE")
    )


class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, primary_key=True, index=True)
    anime_id = Column(Uuid, unique=True)
    title = Column(String(256), unique=True, index=True)
    description = Column(String(512), index=True)
    picture_minio_path = Column(String(256), unique=True, index=True)


class Anime_stat(Base):
    __tablename__ = "anime_stat"

    id = Column(Integer, unique=True, primary_key=True)
    anime_id = Column(
        Uuid, ForeignKey("anime.anime_id", onupdate="CASCADE", ondelete="CASCADE")
    )
    users_started_num = Column(Integer, index=True)
    users_completed_num = Column(Integer, index=True)


class Anime_episode(Base):
    __tablename__ = "anime_episode"

    id = Column(Integer, unique=True, primary_key=True)
    anime_id = Column(
        Uuid, ForeignKey("anime.anime_id", onupdate="CASCADE", ondelete="CASCADE")
    )
    season = Column(Integer, index=True)
    episode = Column(Integer, index=True)
    minio_video_path = Column(String(256), index=True)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, unique=True, primary_key=True)
    anime_id = Column(
        Uuid, ForeignKey("anime.anime_id", onupdate="CASCADE", ondelete="CASCADE")
    )
    comment_id = Column(Integer, unique=True, index=True)
    username = Column(
        String(32), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE")
    )
    body = Column(String(1024))


class UserAnimeStarsCount(Base):
    __tablename__ = "user_anime_stars_count"

    id = Column(Integer, unique=True, primary_key=True)
    username = Column(
        String(32), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE")
    )
    anime_id = Column(
        Uuid, ForeignKey("anime.anime_id", onupdate="CASCADE", ondelete="CASCADE")
    )
    stars = Column(Integer)

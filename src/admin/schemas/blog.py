from pydantic.types import datetime as PDdate
from pydantic import BaseModel, validator
from uuid import UUID
from datetime import datetime, timezone


class NewsModel(BaseModel):
    id_news: UUID
    title: str
    created_at: datetime
    image_path: str


class SingleNewsModel(NewsModel):
    description: str


class NewsPatch(BaseModel):
    title: str
    description: str
    image_path: str
    created_at: PDdate

    @validator("created_at", pre=True)
    def validate_created_at(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        if v is not None and v.tzinfo is not None:  # Check if datetime is offset-aware
            v = v.replace(tzinfo=None)  # Remove timezone information
        return v


class NewsCreate(BaseModel):
    title: str
    created_at: datetime = datetime.now(timezone.utc).replace(
        tzinfo=None
    )  # Set timezone information to None
    description: str
    image_path: str

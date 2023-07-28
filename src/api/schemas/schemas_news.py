from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class OneNews(BaseModel):
    title: str
    published_at: datetime
    id_news: UUID
    sentence: str
    image: str

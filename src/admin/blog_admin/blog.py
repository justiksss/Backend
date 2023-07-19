from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.schemas.blog import NewsModel, SingleNewsModel
from src.database.models import News


class BlogPanel:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_bulk_blog(self, page: int, per_page: int) -> List[NewsModel]:
        offset = (page - 1) * per_page

        stmt = select(News.id_news, News.title, News.created_at, News.description, News.image_path)
        stmt = stmt.limit(per_page).offset(offset)

        res = await self.db.execute(stmt)

        blogs = []
        for row in res:
            blog_data = {
                "id_news": row.id_news,
                "title": row.title,
                "created_at": row.created_at or datetime.utcnow(),
                "image_path": row.image_path or "",
            }
            blogs.append(NewsModel(**blog_data))

        return blogs

    async def get_one(self, uuid:UUID) -> SingleNewsModel:
        stmt = select(News.id_news, News.title, News.created_at, News.description, News.image_path).where(News.id_news == uuid)

        query = await self.db.execute(stmt)
        res = query.one()

        return SingleNewsModel(
            description=res.description,
            id_news=res.id_news,
            created_at=res.created_at,
            title=res.title,
            image_path=res.image_path
        )











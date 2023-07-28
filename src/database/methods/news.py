from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import News
from sqlalchemy import select, delete
from typing import Union, List
from uuid import UUID
from src.api.schemas.schemas_news import OneNews
from asyncpg.exceptions import UniqueViolationError


class New:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_news_by_id(self, id_news: UUID) -> Union[News, str]:
        query = select(News).where(News.id_news == id_news)

        selected = await self.db_session.execute(query)
        row = selected.fetchone()

        if row is not None:
            return row[0]

    async def delete_all_posts(self):
        query = delete(News)
        res = await self.db_session.execute(query)

        return res

    async def get_news_preview(self, page_size: int, page: int) -> List[OneNews]:
        offset = (page - 1) * page_size
        selected = (
            select(News)
            .order_by(News.id_news)
            .limit(limit=page_size)
            .offset(offset=offset)
        )
        result = await self.db_session.execute(selected)
        posts = result.scalars().all()

        news_list = []
        for post in posts:
            news = OneNews(
                title=post.title,
                sentence=post.description.split(".")[0],
                id_news=post.id_news,
                published_at=post.created_at,
                image=post.image_path

            )
            news_list.append(news)

        return news_list

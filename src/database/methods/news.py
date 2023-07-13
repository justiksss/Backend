from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import News
from crawlers.get_news import get_info
from sqlalchemy import select, delete
from typing import Union,List
from uuid import UUID
from src.api.schemas.schemas_news import OneNews
from asyncpg.exceptions import UniqueViolationError
class New:
    def __init__(self ,db_session:AsyncSession):
        self.db_session = db_session

    async def add_news(self):
        info = await get_info()

        added_titles = set()

        for post in info:
            title = post["title"]

            # Skip if the title has already been added
            if title in added_titles:
                continue

            news = News(
                title=title,
                image_path=post["image_name"],
                created_at=post["time"],
                description=post["description"]
            )
            query = select(News).where(News.title == news.title)
            result = await self.db_session.execute(query)
            existing_news = result.scalar()

            if not existing_news:
                try:
                    self.db_session.add(news)
                    await self.db_session.flush()
                except UniqueViolationError:
                    # Skip duplicate news entry and continue with the loop
                    continue

            added_titles.add(title)  # Add the title to the set of added titles

        await self.db_session.commit()

        return "News uploaded"

    async def get_news_by_id(self,id_news: UUID) -> Union[News,str]:
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
        offset = (page -1) * page_size
        selected = select(News).order_by(News.id_news).limit(limit=page_size).offset(offset=offset)
        result = await self.db_session.execute(selected)
        posts = result.scalars().all()

        news_list = []
        for post in posts:
            news = OneNews(
                title=post.title,
                sentence=post.description.split(".")[0],
                id_news=post.id_news,
                published_at=post.created_at
            )
            news_list.append(news)

        return news_list











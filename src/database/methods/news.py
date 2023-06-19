from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import News
from crawlers.get_news import get_info
from sqlalchemy import select, delete
from typing import Union,List
from uuid import UUID
from src.api.schemas.schemas_news import OneNews
from sqlalchemy.orm.attributes import instance_dict
from datetime import datetime

class New:
    def __init__(self ,db_session:AsyncSession):
        self.db_session = db_session

    async def add_news(self):

        info = await get_info()

        for _ in range(0,3):

            for post in info:
                news = News(title=post["title"],image_path=post["image_name"],created_at=post["time"],description=post["description"])

                self.db_session.add(news)
        await self.db_session.flush()

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

    async def get_news_preview(self, limit: int, offset: int) -> List[OneNews]:
        query = await self.db_session.scalars(select(News).limit(limit).offset(offset))
        posts = []
        for i in query:
            post = instance_dict(i)
            time = post['created_at'].replace("Published on ","")
            datetime_format = "%d.%m.%Y %H:%M:%S"
            datetime_obj = datetime.strptime(time,datetime_format)
            news = OneNews(title=post["title"], sentence=post['description'].split(".")[0],id_news=post["id_news"],published_at=datetime_obj)
            posts.append(news)

        return posts









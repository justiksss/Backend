from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.methods.news import New
from uuid import UUID

from src.database.models import News


async def post_news(session: AsyncSession):
    async with session.begin():

        news_dal = New(session)

        news = await news_dal.add_news()

        return news


async def get_post_info(session: AsyncSession, id_news: UUID) -> dict:
    async with session.begin():
        news_dal = New(session)

        news = await news_dal.get_news_by_id(id_news)
        path_to_image = f"images/{news.image_path}.png"

        if news is not None:
            return {
                "image":path_to_image,
                "text":news
            }

async def delete_blog_info(session: AsyncSession):
    async with session.begin():
        news_dal = New(session)

        deleted = await news_dal.delete_all_posts()

        return "All deleted"


async def get_page(session: AsyncSession, page_size: int = 3, page: int = 1) -> dict:
    async with session.begin():

        news_dal = New(session)

        selected = await news_dal.get_news_preview(limit=page_size,offset=page)
        length = await session.scalar(select(func.count()).select_from(News))


        return {
            "total_pages": length // page_size,
            "all_posts": selected
        }
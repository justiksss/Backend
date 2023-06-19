from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.api.handlers.news import delete_blog_info, post_news
from src.database.session import get_db

admin_router = APIRouter()


@admin_router.delete("/drop_posts_table")
async def drop_news(db: AsyncSession = Depends(get_db)):
    """Drop schemas posts from table (news)"""
    query = await delete_blog_info(session=db)

    return "All done"


@admin_router.post("/add_new_posts")
async def post_a_news(db: AsyncSession = Depends(get_db)):
    """Run crawlers to add new posts , (5-10 minutes to finish)"""
    try:
        return await post_news(session=db)
    except IntegrityError as err:
        raise HTTPException(detail=f"{err}",status_code=503)
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.admin.blog_admin.blog import BlogPanel
from fastapi import APIRouter, Query, Depends, HTTPException

from src.admin.schemas.blog import NewsPatch, NewsCreate
from src.api.handlers.login import get_current_user_from_token
from src.database.models import News
from src.database.session import get_db
from uuid import UUID

admin_blog = APIRouter()


@admin_blog.get("/blog_list")
async def get_news(page_size: int = Query(5, ge=1),page: int = Query(1, ge=1), db: AsyncSession = Depends(get_db),user=Depends(get_current_user_from_token)):
    if user.roles != "Admin":
        raise HTTPException(detail="Permission denied",status_code=403)
    blog_panel = BlogPanel(db=db)

    res = await blog_panel.get_bulk_blog(page=page,per_page=page_size)

    return res

@admin_blog.get("/post")
async def get_one(uuid: UUID,db: AsyncSession = Depends(get_db),user=Depends(get_current_user_from_token)):
    if user.roles != "Admin":
        raise HTTPException(detail="Permission denied",status_code=403)
    blog_panel = BlogPanel(db=db)

    res = await blog_panel.get_one(uuid=uuid)

    return res

@admin_blog.patch("/post")
async def update_news(news_id: UUID, data: NewsPatch, db=Depends(get_db),user=Depends(get_current_user_from_token)):
    if user.roles != "Admin":
        raise HTTPException(detail="Permission denied",status_code=403)
    async with db.begin():
        stmt = select(News).where(News.id_news == news_id)
        result = await db.execute(stmt)
        news = result.scalar()

        if news is None:
            raise HTTPException(status_code=404, detail="News not found")

        # Update only the fields that are present in the request data
        for field, value in data.model_dump().items():
            if hasattr(News, field):
                setattr(news, field, value)

    await db.commit()
    await db.refresh(news)
    return news

@admin_blog.post("/create")
async def create_news(news_data: NewsCreate, db=Depends(get_db),user=Depends(get_current_user_from_token)):
    if user.roles != "Admin":
        raise HTTPException(detail="Permission denied",status_code=403)
    async with db.begin():
        news = News(**news_data.model_dump())
        db.add(news)
        await db.flush()  # Use flush() instead of commit()
        await db.refresh(news)
        return news


@admin_blog.delete("/blog/{news_id}", response_model=None)
async def delete_news(news_id: UUID, db: AsyncSession=Depends(get_db), user=Depends(get_current_user_from_token)):
    if user.roles != "Admin":
        raise HTTPException(detail="Permission denied", status_code=403)


    stmt = select(News).where(News.id_news==news_id)
    news = await db.scalar(stmt)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")

    await db.delete(news)
    await db.flush()

    return news_id
from fastapi import APIRouter,Depends,HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.handlers.news import get_post_info,get_page
from fastapi.responses import FileResponse
from src.database.session import get_db
from uuid import UUID

news_router = APIRouter()


@news_router.get("/image", response_class=FileResponse)
async def get_image_by_id_post(id_news: UUID , db: AsyncSession = Depends(get_db)):
    """Get image by id(UUID)"""
    blogs = await get_post_info(id_news=id_news, session=db)
    image = blogs["image"]
    if blogs is None:
        raise HTTPException(status_code=404,detail=f"News with id {id_news} not found")
    return image


@news_router.get("/post")
async def get_text_by_id_post(id_news: UUID, db:AsyncSession = Depends(get_db)):

    post = await get_post_info(id_news=id_news, session=db)

    text = post["text"]

    if text is None:
        raise HTTPException(status_code=404,detail=f"News with id {id_news} not found")
    return text



@news_router.get("/page")
async def view_page(page_size: int = Query(5, ge=1), page: int = Query(1, ge=1), db: AsyncSession = Depends(get_db)):
    posts = await get_page(page_size=page_size,page=page,session=db)

    return posts
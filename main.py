
from src.routers.user import user_router
from src.routers.login import login_router
from src.routers.news import news_router
from src.routers.admin_routers import admin_router
from fastapi import FastAPI
# from src.routers.job import job_router


app = FastAPI(
    title="Jobs-Prague"
)
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(news_router,prefix="/news", tags=["news"])
# app.include_router(job_router, prefix="/job", tags=['job'])


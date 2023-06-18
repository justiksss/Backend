from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.handlers.jobs import upload_jobs
from app.database.session import get_db
from sqlalchemy.exc import IntegrityError

job_router = APIRouter()


@job_router.post("/add_jobs")
async def post_a_jobs(db: AsyncSession = Depends(get_db)):
    """Run crawlers to add new jobs , (long task for 15-20 for full upload)"""
    try:
        return await upload_jobs(session=db)
    except IntegrityError as err:
        raise HTTPException(detail=f"{err}",status_code=503)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.handlers.jobs import get_one_job, get_jobs_view, main_search
from src.database.session import get_db
from sqlalchemy.exc import IntegrityError
from src.api.schemas.filters import Params
job_router = APIRouter()


# @job_router.post("/add_jobs")
# async def post_a_jobs(db: AsyncSession = Depends(get_db)):
#     """Run crawlers to add new jobs , (long task for 15-20 for full upload)"""
#     try:
#         return await upload_jobs(session=db)
#     except IntegrityError as err:
#         raise HTTPException(detail=f"{err}",status_code=503)


@job_router.get("/get_job")
async def get_job(uuid: UUID, db: AsyncSession = Depends(get_db)):
    """Get one job by uuid"""

    return await get_one_job(session=db,uuid=uuid)


@job_router.get("/list_jobs")
async def get_page_jobs(limit: int = 12, offset: int = 0, db: AsyncSession = Depends(get_db)):
    "Get job view"
    return await get_jobs_view(session=db,limit=limit,offset=offset)


@job_router.get("/filters")
async def filters_search(params: Params = Depends(), db:AsyncSession = Depends(get_db)):
    """Main search"""
    jobs = await main_search(param=params,session=db)

    return jobs
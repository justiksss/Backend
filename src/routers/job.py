from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.handlers.jobs import get_one_job, main_search,get_all_companies
from src.database.session import get_db
from src.api.schemas.filters import Params
job_router = APIRouter()


# @job_router.post("/add_jobs")
# async def post_a_jobs(db: AsyncSession = Depends(get_db)):
#     """Run crawlers to add new jobs , (long task for 15-20 for full upload)"""
#
#     return await upload_jobs(session=db)



@job_router.get("/get_job")
async def get_job(uuid: UUID, db: AsyncSession = Depends(get_db)):
    """Get one job by uuid"""

    return await get_one_job(session=db,uuid=uuid)



@job_router.get("/filters")
async def filters_search(limit: int = 5, offset: int = 1, params: Params = Depends(), db:AsyncSession = Depends(get_db)):
    """Main search, with params:\n
    days ago params - insert int and get all jobs with less then your integer \n
    job-type -  can be : job_translate = {
                "Full time",
                "Part-time job",
                "Contract",
                "Temporary work"
            } \n
    keyword search by this from title of job and text of each \n
    company get from another endpoint \n
    return is dict{
    page: int
    total_count: int
    jobs[...]
    }

    """
    jobs = await main_search(params=params,session=db,per_page=limit,page=offset)

    return jobs

@job_router.get("/get_company")
async def all_companies(db: AsyncSession = Depends(get_db)) -> List[str]:
    """Get list with all company (List[str])"""

    companies = await get_all_companies(db=db)

    return companies

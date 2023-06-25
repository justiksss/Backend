from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from src.database.methods.jobs import JobsDal
from src.database.models import Jobs
from uuid import UUID
from sqlalchemy import select,func
from src.api.schemas.filters import Params
from fastapi import Query
# async def upload_jobs(session: AsyncSession) -> str:
#
#     async with session.begin():
#
#         jobs_dal = JobsDal(session)
#
#         jobs_res = await jobs_dal.upload_jobs()
#
#         return jobs_res


async def get_one_job(session: AsyncSession, uuid: UUID) -> Union[Jobs, str]:

    async with session.begin():

        jobs_dal = JobsDal(session)

        jobs_select = await jobs_dal.get_job_by_uuid(uuid=uuid)

        if jobs_select is None:
            return f"Job with {uuid} not found"

        return jobs_select


async def get_jobs_view(session: AsyncSession,limit: int, offset: int) -> Union[dict, str]:

    async with session.begin():
        jobs_dal = JobsDal(db_session=session)

        jobs_page = await jobs_dal.get_page(limit=limit,offset=offset)

        length = await session.scalar(select(func.count()).select_from(Jobs))

        if jobs_page is None:
            return "Jobs not found"

        return {"pages": length // limit,"jobs":jobs_page}




async def main_search(session: AsyncSession, param: Params, limit: int, offset: int) -> dict:
    async with session.begin():
        query = select(Jobs)
        if param.keyword:
            query = query.where(Jobs.name.ilike(f'%{param.keyword}%'))
        if param.job_type:
            query = query.where(Jobs.job_type == param.job_type)
        if param.company_name:
            query = query.where(Jobs.company_name.ilike(f'%{param.company_name}%'))
        if param.days_ago_posted:
            query = query.where(Jobs.posted_days_ago <= param.days_ago_posted)

        count_query = select(func.count()).select_from(query.alias()).scalar()

        total_results = await session.execute(count_query)

        query = query.limit(limit).offset(offset)
        result = await session.execute(query)
        jobs = result.scalars().all()

        results = []
        for job in jobs:
            results.append({
                'id': job.id_job,
                'keyword': job.name,
                'job_type': job.job_type,
                'company_name': job.company_name,
                'days_ago_posted': job.posted_days_ago
            })

        pages = total_results // limit

        return {"pages": pages, "jobs": results}



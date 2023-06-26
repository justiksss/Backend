import math

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from src.database.methods.jobs import JobsDal
from src.database.models import Jobs
from uuid import UUID
from sqlalchemy import select,func, or_
from src.api.schemas.filters import Params


# async def upload_jobs(session: AsyncSession) -> str:
#
#
#
#     jobs_dal = JobsDal(session)
#
#     jobs_res = await jobs_dal.upload_jobs()
#
#     return jobs_res


async def get_one_job(session: AsyncSession, uuid: UUID) -> Union[dict, str]:

    async with session.begin():

        jobs_dal = JobsDal(session)

        jobs_select = await jobs_dal.get_job_by_uuid(uuid=uuid)

        if jobs_select is None:
            return f"Job with {uuid} not found"

        return jobs_select






async def main_search(page, per_page, params: Params, session: AsyncSession):
    # Convert company_name and keyword to lowercase for case-insensitive search
    if params.company_name is not None:
        company_name = params.company_name.lower()
    else:
        company_name = None

    if params.keyword is not None:
        keyword = params.keyword.lower()
    else:
        keyword = None

    if params.job_type is not None:
        job_type = params.job_type.lower()
    else:
        job_type = None

    # Create an asynchronous session
    async with session.begin():
        # Create a base query
        query = select(Jobs)

        if params.days_ago_posted is not None:
            # Calculate the date 'days_ago_posted' days ago from the current date
            query = query.where(Jobs.posted_days_ago >= params.days_ago_posted)

        if company_name:
            query = query.where(func.lower(Jobs.company_name).like(f'%{company_name}%'))

        if keyword:
            query = query.where(
                or_(
                    func.lower(Jobs.company_name).like(f'%{keyword}%'),
                    func.lower(Jobs.description).like(f'%{keyword}%')
                )
            )

        if job_type:
            query = query.where(func.lower(Jobs.job_type).like(f'%{job_type}%'))

        # Execute the query
        result = await session.execute(query)

        # Fetch the jobs
        jobs = result.scalars().all()

        # Calculate total count after filters
        count_query = select(func.count()).select_from(query.alias("subquery"))
        total_count = await session.scalar(count_query)

        # Calculate total pages
        total_pages = math.ceil(total_count / per_page)

        # Apply pagination
        query = query.limit(per_page).offset((page - 1) * per_page)
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

        return {"total_pages": total_pages, "total_count": total_count, "jobs": results}


async def get_all_companies(db: AsyncSession) -> list:
    async with db.begin():
        companies = await db.execute(select(Jobs.company_name).distinct())
        companies = [company for company in companies.scalars().all()]
        return companies




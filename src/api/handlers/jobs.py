import math
from sqlalchemy.sql.expression import desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from src.database.methods.jobs import JobsDal
from src.database.models import Jobs
from uuid import UUID
from sqlalchemy import select, func, or_, and_
from src.api.schemas.filters import Params
from src.api.schemas.schemas_jobs import Job, Jobs_AddView


async def get_one_job(session: AsyncSession, uuid: UUID) -> Union[dict, str]:
    async with session.begin():
        jobs_dal = JobsDal(db_session=session)

        jobs_select = await jobs_dal.get_job_by_uuid(uuid=uuid)

        if jobs_select is None:
            return f"Job with {uuid} not found"

        return jobs_select


async def main_search(params: Params, session: AsyncSession):
    company_name = (
        params.company_name.lower() if params.company_name != "string" else None
    )
    keyword = (
        params.keyword.lower().replace(" ", "+") if params.keyword != "string" else None
    )
    job_type = params.job_type.lower() if params.job_type != "string" else None

    async with session.begin():
        query = select(Jobs).where(Jobs.is_active == True)

        if params.days_ago_posted is not None and params.days_ago_posted != "":
            query = query.where(Jobs.posted_days_ago <= int(params.days_ago_posted))

        if company_name:
            query = query.where(func.lower(Jobs.company_name).like(f"%{company_name}%"))

        if keyword:
            keyword_words = keyword.split("+")

            keyword_conditions = [
                or_(
                    func.lower(Jobs.company_name).like(f"%{word}%"),
                    func.lower(Jobs.description).like(f"%{word}%"),
                )
                for word in keyword_words
            ]

            query = query.where(and_(*keyword_conditions))

        if job_type:
            query = query.where(func.lower(Jobs.job_type).like(f"%{job_type}%"))

        if params.sort_by == "New jobs":
            query = query.order_by(asc(Jobs.posted_days_ago))
        elif params.sort_by == "Name descending":
            query = query.order_by(desc(Jobs.name))
        elif params.sort_by == "Name ascending":
            query = query.order_by(asc(Jobs.name))

        count_query = select(func.count()).select_from(query.alias("subquery"))
        total_count = await session.scalar(count_query)

        total_pages = math.ceil(total_count / params.per_page)

        query = query.limit(params.per_page).offset((params.page - 1) * params.per_page)
        result = await session.execute(query)
        jobs = result.scalars().all()

        results = []
        for job in jobs:
            results.append(
                {
                    "id": job.id_job,
                    "keyword": job.name,
                    "job_type": job.job_type,
                    "company_name": job.company_name,
                    "days_ago_posted": job.posted_days_ago,
                    "image": job.logo,
                }
            )

        return {"total_pages": total_pages, "total_count": total_count, "jobs": results}


async def get_all_companies(db: AsyncSession) -> list:
    async with db.begin():
        companies = await db.execute(select(Jobs.company_name).distinct())
        companies = [company for company in companies.scalars().all()]
        return companies


async def add_job(session: AsyncSession, job: Job):
    description: str = (
        "<ul>"
        + "".join(
            [
                f"<li>{i}</li>"
                for i in [
                    job.salary,
                    job.contact_email,
                    job.twitter,
                    job.video,
                    job.remote_position,
                ]
                if i is not None
            ]
        )
        + "</ul>"
        + job.description
    )
    job_template: Jobs = Jobs(
        name=job.title,
        link=job.link_for_contact,
        job_type=job.job_type,
        location=job.location,
        description=description,
        company_name=job.company_name,
        logo=job.logo,
    )
    async with session.begin():
        job_dal = JobsDal(db_session=session)

        new_job = await job_dal.add_job_after_payment(job=job_template)

        return Jobs_AddView(id_job=new_job.id_job, name=new_job.name)


async def get_image_by_uuid(session: AsyncSession, id_news: UUID) -> dict:
    async with session.begin():
        news_dal = JobsDal(session)

        jobs = await news_dal.get_job_by_uuid(id_news)
        path = jobs.get("logo")
        path_to_image = (
            f"/Users/oleksiiyudin/Desktop/Backend/images/images_for_job/{path}"
        )
        if jobs is not None:
            return {"image": path_to_image}


async def get_image_by_name(filename: str) -> dict:
    path_to_image = (
        f"/Users/oleksiiyudin/Desktop/Backend/images/images_for_job/{filename}"
    )

    return {"image": path_to_image}


async def set_active_job(uuid: UUID, session: AsyncSession) -> Union[UUID, None]:
    async with session.begin():
        # Select the job with the specified UUID
        job = select(Jobs).where(Jobs.id_job == uuid)

        # Execute the select query
        result = await session.execute(job)

        # Retrieve the job
        job = result.scalar()

        if job is not None:
            # Update the is_active field
            job.is_active = True

            # Commit the changes
            await session.commit()

            return uuid
        else:
            return None

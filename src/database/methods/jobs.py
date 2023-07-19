from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import instance_dict
from src.database.models import Jobs
from uuid import UUID
from sqlalchemy import select
from typing import List
from src.api.schemas.schemas_jobs import JobsView, Jobs_AddView


class JobsDal:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_job_by_uuid(self, uuid: UUID) -> dict:
        query = select(Jobs).where(Jobs.id_job == uuid)

        selected = await self.db_session.execute(query)
        row = selected.fetchone()

        if row is not None:
            job = row[0]  # Access the Jobs object from the tuple

            job_dict = {
                "id_job": job.id_job,
                "name": job.name,
                "link": job.link,
                "company_name": job.company_name,
                "job_type": job.job_type,
                "location": job.location,
                "description": job.description,
                "logo": job.logo,
                "posted_days_ago": job.posted_days_ago,
            }

            return job_dict

    async def get_page(self, limit: int, offset: int) -> List[JobsView]:
        query = await self.db_session.scalars(select(Jobs).limit(limit).offset(offset))
        posts = []
        for i in query:
            jobs_extend = instance_dict(i)

            job = JobsView(
                id_job=jobs_extend["id_job"],
                name=jobs_extend["name"],
                logo=jobs_extend["logo"],
                location="Prague",
                company_name=jobs_extend["company_name"],
            )
            posts.append(job)

        return posts

    async def get_companies(self) -> List:
        column_values = await self.db_session.execute(select(Jobs.company_name))
        values = [value for value, in column_values.all()]

        return values

    async def add_job_after_payment(self, job: Jobs) -> Jobs_AddView:
        new_job = Jobs(
            name=job.name,
            description=job.description,
            posted_days_ago=1,
            company_name=job.company_name,
            job_type=job.job_type,
            location=job.location,
            logo=job.logo,
            link=job.link,
            is_active=False,
        )
        self.db_session.add(new_job)
        await self.db_session.flush()

        return Jobs_AddView(name=new_job.name, id_job=new_job.id_job)

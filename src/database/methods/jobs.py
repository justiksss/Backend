from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.base import instance_dict


from src.database.models import Jobs
from uuid import UUID
from sqlalchemy import select
from typing import List
from src.api.schemas.schemas_jobs import JobsView


def job_to_dict(job):
    job_dict = {
        "company_name": job.company_name,
        "link": job.link,
        "location": job.location,
        "logo": job.logo,
        "job_type": job.job_type,
        "id_job": job.id_job,
        "name": job.name,
        "description": job.description,
        "posted_days_ago": job.posted_days_ago
    }
    return job_dict


class JobsDal:
    def __init__(self,db_session: AsyncSession):
        self.db_session = db_session

    # async def upload_jobs(self):
    #     jobs = get_jobs()
    #
    #     for job in jobs:
    #         if job["name"] and job["link"] and job["company_name"] is not None:
    #             new_job = Jobs(
    #                 link=job["link"],
    #                 name=job["name"],
    #                 company_name=job["company_name"],
    #                 job_type=job["job_type"],
    #                 location=job["location"],
    #                 description=job["description"],
    #                 logo=job['logo'],
    #                 posted_days_ago = job["post_days_ago"]
    #                 )
    #             self.db_session.add(new_job)
    #
    #     await self.db_session.flush()
    #
    #     return "Jobs uploaded"

    async def get_job_by_uuid(self, uuid: UUID) -> dict:
        query = select(Jobs).where(Jobs.id_job == uuid)
        selected = await self.db_session.execute(query)
        row = selected.fetchone()

        if row is not None:
            job_dict = job_to_dict(row[0])
            return job_dict

    async def get_page(self, limit: int, offset: int) -> List[JobsView]:

        query = await self.db_session.scalars(select(Jobs).limit(limit).offset(offset))
        posts = []
        for i in query:
            jobs_extend = instance_dict(i)

            posts.append(job)

        return posts

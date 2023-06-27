from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import instance_dict
from src.database.models import Jobs
from uuid import UUID
from sqlalchemy import select
from typing import List
from src.api.schemas.schemas_jobs import JobsView


class JobsDal:
    def __init__(self,db_session: AsyncSession):
        self.db_session = db_session

    # async def upload_jobs(self):
    #
    #     page_id = 0
    #
    #     for k in range(300):
    #             try:
    #                 job = search_all(page_id)
    #             except NoSuchElementException:
    #                 page_id += 10
    #
    #
    #             sleep(2)
    #             page_id += 10
    #             sleep(3)
    #
    #
    #             if job["name"] and job["link"] and job["company_name"] is not None:
    #                 existing_job = await self.db_session.execute(
    #                     select(Jobs).where(Jobs.link == job["link"])
    #                 )
    #                 existing_job = existing_job.scalar_one_or_none()
    #
    #                 if existing_job is None:
    #
    #                     new_job = Jobs(
    #                         link=job["link"],
    #                         name=job["name"],
    #                         company_name=job["company_name"],
    #                         job_type=job["job_type"],
    #                         location=job["location"],
    #                         description=job["description"],
    #                         logo=job['logo'],
    #                         posted_days_ago = job["post_days_ago"]
    #                         )
    #
    #                     try:
    #                         self.db_session.add(new_job)
    #                         await self.db_session.flush()
    #                         await self.db_session.commit()
    #
    #                     except IntegrityError as e:
    #                         if "jobs_name_key" in str(e):
    #                             # Handle duplicate job name error
    #                             await self.db_session.rollback()
    #                             continue
    #                         else:
    #                             # Handle other IntegrityErrors
    #                             raise





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

            job = JobsView(id_job=jobs_extend["id_job"],name=jobs_extend["name"],logo=jobs_extend["logo"],location="Prague",company_name=jobs_extend["company_name"])
            posts.append(job)

        return posts

    async def get_companies(self) -> List:

        column_values = await self.db_session.execute(
            select(Jobs.company_name)
        )
        values = [value for value, in column_values.all()]

        return values

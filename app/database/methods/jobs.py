from sqlalchemy.ext.asyncio import AsyncSession
from crawlers.get_jobs import main
from app.database.models import Jobs

class JobsDal:
    def __init__(self,db_session: AsyncSession):
        self.db_session = db_session

    async def upload_jobs(self):
        jobs = main()

        for job in jobs:
            new_job = Jobs(
                link=job["link"],
                name=job["name"],
                link_name=job["link_name"],
                job_type=job["job_type"],
                location=job["location"],
                description=job["description"],
                logo=job['logo_link']
                )
            self.db_session.add(new_job)

        await self.db_session.flush()

        return "Jobs uploaded"


from sqlalchemy.ext.asyncio import AsyncSession

from app.database.methods.jobs import JobsDal


async def upload_jobs(session: AsyncSession) -> str:

    async with session.begin():

        jobs_dal = JobsDal(session)

        jobs_res = await jobs_dal.upload_jobs()

        return jobs_res

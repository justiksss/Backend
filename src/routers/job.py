import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.handlers.jobs import get_one_job, main_search,get_all_companies,add_job
from src.database.session import get_db
from src.api.schemas.filters import Params
from src.api.schemas.schemas_jobs import Job
from fastapi import File
import os
from fastapi.responses import FileResponse

job_router = APIRouter()


@job_router.get("/get_job")
async def get_job(uuid: UUID, db: AsyncSession = Depends(get_db)):
    """Get one job by uuid"""

    return await get_one_job(session=db,uuid=uuid)



@job_router.post("/search")
async def search_jobs(params: Params, session: AsyncSession = Depends(get_db)):

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
    }\n
    sort by can be: {"New jobs","Name ascending","Name descending"}\n
    Name ascending -> first letter A
    Name descending -> first letter Z
    New jobs -> start from posted days ago 1
    """
    jobs = await main_search(params=params,session=session)

    return jobs

@job_router.get("/get_company")
async def all_companies(db: AsyncSession = Depends(get_db)) -> List[str]:
    """Get list with all company (List[str])"""

    companies = await get_all_companies(db=db)

    return companies


@job_router.post("/add_job")
async def add_job_after_pay(body: Job,db: AsyncSession = Depends(get_db)):
    """Example perfect job:\n{
  "title": "Software Engineer", unique \n
  "link_for_contact": "https://example.com/contact",\n
  "company_name": "ABC Company",\n
  "job_type": "Full-time",{ "Full time", "Part-time job", "Contract", "Temporary work" } \n
  "location": "New York",\n
  "description": "Job description goes here",\n
  "remote_position": "Yes", Optional\n
  "salary": 100000,Optional\n
  "contact_email": "contact@example.com",Optional\n
  "video": "https://example.com/video",Optional\n
  "twitter": "@example" \n
   By default this job is non-active

}"""

    new_job_response = await add_job(session=db, job=body)
    return new_job_response


@job_router.post("/image/{logo}")
async def upload_image(file: UploadFile = File(None)):
    """Takes image in png format and add to dir with images.\n
    if send None , logo will be by default:https://cdn-icons-png.flaticon.com/512/306/306424.png \n
    ONLY PNG"""
    if file is None:
        return {"default_image_url": "https://cdn-icons-png.flaticon.com/512/306/306424.png"}

    if file.content_type.startswith("image/png"):
        destination_dir = "images"
        os.makedirs(destination_dir, exist_ok=True)


        file_path = os.path.join(destination_dir, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return {"message": 200,
                "name": f"https://teste-cmg2.onrender.com/job/get_image?file_name={file.filename}"
                }

@job_router.get("/get_image")
async def get_image(file_name: str):
    """Takes file name and if image with this name exist return a link with image \n
    if not raise http exceptions"""
    file_path = "images/" + file_name

    if file_name.endswith(".png"):
        return FileResponse(file_path, media_type="image/png")
    else:
        return {"error": "PNG file not found"}








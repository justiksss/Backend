from pydantic import BaseModel
from pydantic import HttpUrl
from uuid import UUID
from pydantic import EmailStr
from typing import Optional
from fastapi import UploadFile
class Job(BaseModel):
    title: str
    link_for_contact: str
    company_name: str
    job_type: str
    location: str
    description: str
    remote_position: Optional[str] = None
    salary: Optional[int] = None
    contact_email: Optional[str] = None
    video: Optional[HttpUrl] = None
    twitter: Optional[str] = None
    logo: str



class JobsView(BaseModel):
    id_job: UUID
    name: str
    logo: HttpUrl
    company_name: str
    location: str


class Jobs_AddView(BaseModel):
    id_job: UUID
    name: str

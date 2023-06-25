from pydantic import BaseModel
from pydantic import HttpUrl
from uuid import UUID
class Job(BaseModel):
    name: str
    link: HttpUrl
    link_name: str
    job_type: str
    location: str
    description: str
    logo: str


class JobsView(BaseModel):
    id_job: UUID
    name: str
    logo: HttpUrl
    company_name: str
    location: str

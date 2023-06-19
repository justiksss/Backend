from pydantic import BaseModel
from pydantic import HttpUrl

class Job(BaseModel):
    name: str
    link: HttpUrl
    link_name: str
    job_type: str
    location: str
    description: str
    logo: str
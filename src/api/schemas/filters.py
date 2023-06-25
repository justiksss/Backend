from pydantic import BaseModel
from typing import Optional,List

class Params(BaseModel):
    keyword: Optional[str] = None
    job_type: Optional[str] = None
    company_name: Optional[str] = None
    days_ago_posted: Optional[int] = None
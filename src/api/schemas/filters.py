from pydantic import BaseModel
from typing import Optional,List


class Params(BaseModel):
    per_page: int = 12
    page: int = 1
    keyword: str = ''
    job_type: str = ''
    company_name: str = ''
    days_ago_posted: str = ''
    sort_by: str = ''

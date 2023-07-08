import uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Boolean, UUID, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql.array import ARRAY

Base = declarative_base()


class User(Base):
    __tablename__= "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(String(50), nullable=False)
    posted_jobs = Column(ARRAY(String), nullable=True)



class News(Base):
    __tablename__ = "news"

    id_news = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)

    title = Column(Text, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(Text, nullable=False)


class Jobs(Base):
    __tablename__ = "jobs"

    id_job = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)

    name = Column(Text, nullable=False, unique=True)
    link = Column(String, nullable=False)
    company_name = Column(String, nullable=False, index=True)
    job_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    logo = Column(String, nullable=False)
    posted_days_ago = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)





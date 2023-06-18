import uuid
from enum import Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Boolean, UUID, Integer,TEXT,Text

Base = declarative_base()


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"


class User(Base):
    __tablename__= "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=False)

    @property
    def is_superadmin(self) -> bool:
        return PortalRole.ROLE_PORTAL_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return {*self.roles, PortalRole.ROLE_PORTAL_ADMIN}

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            return {role for role in self.roles if role != PortalRole.ROLE_PORTAL_ADMIN}


class News(Base):
    __tablename__ = "news"

    id_news = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(Text, nullable=False)


class Jobs(Base):
    __tablename__ = "jobs"

    id_job = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    link = Column(String, nullable=False)
    link_name = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    logo = Column(String, nullable=False)
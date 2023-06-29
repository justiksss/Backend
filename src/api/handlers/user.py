from typing import Union
from src.api.schemas.old_schemas import UserCreate, ShowUser
from src.database.methods.userdal import UserDAL
from uuid import UUID
from src.database.models import User
from src.security.hashing import Hasher
from sqlalchemy.ext.asyncio import AsyncSession

async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():

        user_dal = UserDAL(session)

        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
            roles="Default user"
        )
        return ShowUser(
            user_id = user.user_id,
            name = user.name,
            surname= user.surname,
            email = user.email,
            is_active=user.is_active
        )

async def _delete_user(user_id, session) -> Union[str, None]:
    async with session.begin():

        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(user_id=user_id)

        return deleted_user_id


async def _get_user_by_id(user_id, session) -> Union[UUID, None]:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id)
            if user is not None:
                return user


async def _update_user(updated_user_params: dict, user_id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user_id


async def change_user_role(uuid: UUID, new_role: str, session:AsyncSession) -> User:
    async with session.begin():

        user_dal = UserDAL(session)

        new_user_role = await user_dal.change_user_role(uuid=uuid,new_role=new_role)

        return new_user_role
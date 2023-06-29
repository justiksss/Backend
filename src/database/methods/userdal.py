from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from src.database.models import User
from typing import Union,List
from uuid import UUID


class Dal:
    def __init__(self ,db_session:AsyncSession):
        self.db_session = db_session


class UserDAL(Dal):
    async def create_user(self, name: str, surname: str, email: str, hashed_password: str, roles: str) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
            roles=roles
        )

        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> str:
        query = delete(User).where(User.user_id == user_id)
        # query = select(User).where(and_(User.user_id == user_id, User.is_active == True)).value(is_active=False).returning(User.user_id)
        res = await self.db_session.execute(query)

        return f"User with {user_id} is deleted"

    async def get_user_by_id(self, user_id:UUID) -> Union[UUID,None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


    async def get_user_by_email(self, email: str) -> Union[User, None]:

        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


    async def change_user_role(self,uuid: UUID, new_role: str) -> User:

        query = select(User).where(User.user_id == uuid)

        result = await self.db_session.execute(query)

        user = result.scalar_one_or_none()

        if user:
            user.roles = new_role

        await self.db_session.commit()

        return User(
            email=user.email,
            roles=user.roles
        )
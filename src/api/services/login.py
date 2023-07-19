from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Union
from src.database.models import User
from src.database.session import get_db
from src.security.hashing import Hasher
from src.database.methods.userdal import UserDAL
from fastapi.security import OAuth2PasswordBearer
from config import ALGORITM, SECRET_KEY
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_email_for_auth(email: str, db: AsyncSession):
    async with db.begin():
        user_dal = UserDAL(db)
        return await user_dal.get_user_by_email(email)


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITM)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        raise credentials_exception
    return user


async def authenticate_user(
    email: str, password: str, db: AsyncSession
) -> Union[User, bool]:
    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.api.handlers.user import (
    _delete_user,
    _create_new_user,
    _get_user_by_id,
    _update_user,
    change_user_role,
)
from src.database.models import User
from src.database.session import get_db
from src.api.schemas.old_schemas import (
    UserCreate,
    ShowUser,
    UpdatedUserResponse,
    UpdateUserRequest,
)
from uuid import UUID
from fastapi import HTTPException
from src.api.services.login import get_current_user_from_token
from logging import getLogger
from pydantic import EmailStr
from src.api.handlers.login import authenticate_user

user_router = APIRouter()
logger = getLogger(__name__)


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/")
async def delete_user(
    user_id,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    user_for_deletion = await _get_user_by_id(user_id, db)

    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    return f"User with this id:{user_id} removed"


@user_router.get("/")
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user


@user_router.patch("/change_role")
async def change_user_role_by_uuid(
    user_id: UUID, new_role: str, db: AsyncSession = Depends(get_db)
):
    """Can be ("Default_user","Subscriber_TIER_1","Subscriber_TIER_2","Subscriber_TIER_3") \n
    response changed_role : user email

    """
    user_role_list = (
        "Default_user",
        "Subscriber_TIER_1",
        "Subscriber_TIER_2",
        "Subscriber_TIER_3",
        "Admin"
    )
    if new_role not in user_role_list:
        raise HTTPException(status_code=404, detail=f"Not found role:{new_role}")

    changed_role = await change_user_role(uuid=user_id, session=db, new_role=new_role)

    if changed_role is None:
        raise HTTPException(
            status_code=404, detail=f"User with this id {user_id} not found"
        )

    return changed_role


@user_router.get("/check_permission")
async def check_user_permission(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    user_role_list = ("Subscriber_TIER_1", "Subscriber_TIER_2", "Subscriber_TIER_3")
    if current_user.roles not in user_role_list:
        raise HTTPException(status_code=403, detail="User is not a subscriber")
    else:
        return f"User with {current_user.user_id} id is a subscriber"


@user_router.get("/check_user")
async def check_user(
    email: EmailStr, password: str, db: AsyncSession = Depends(get_db)
) -> dict:
    user = await authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"email": user.email, "id": user.user_id}

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.api.handlers.user import _delete_user, _create_new_user, _get_user_by_id, _update_user, check_user_permissions
from src.database.models import User
from src.database.session import get_db
from src.api.schemas.old_schemas import UserCreate, ShowUser, UpdatedUserResponse, UpdateUserRequest
from uuid import UUID
from fastapi import HTTPException
from src.api.services.login import get_current_user_from_token
from logging import getLogger

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
    if user_id != current_user.user_id:
        if check_user_permissions(target_user=user_for_update, current_user=current_user):
            raise HTTPException(status_code=403, detail="Forbidden.")
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
        raise HTTPException(status_code=503,detail=f"Database error: {err}")


@user_router.delete("/")
async def delete_user(user_id, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    user_for_deletion = await _get_user_by_id(user_id, db)

    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_permissions(target_user=user_for_deletion,current_user=current_user,):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    return f"User with this id:{user_id} removed"


@user_router.get("/")
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    user = await _get_user_by_id(user_id,db)
    if user is None:
        raise HTTPException(status_code=404,detail=f"User with id {user_id} not found")
    return user

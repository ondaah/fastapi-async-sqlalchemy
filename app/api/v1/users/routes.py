from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.db import AsyncSession, database, User
from app.schemas import (
    UserSchema,
    UserCreateSchema,
    UserUpdateFullSchema,
    UserUpdatePartialSchema,
)

from .crud import CRUD

router = APIRouter()


@router.get("/", response_model=list[UserSchema])
async def list_users(session: AsyncSession = Depends(database.get_session)):
    """List all users from the database."""
    return await CRUD.get_users(session)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user_by_id(
    user_id: str, session: AsyncSession = Depends(database.get_session)
):
    user_model = await CRUD.get_user(session, UUID(user_id))
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    return user_model


@router.post("/", response_model=UserSchema)
async def create_user(
    user: UserCreateSchema, session: AsyncSession = Depends(database.get_session)
):
    user_model = User(username=user.username, email=user.email, password=user.password)
    return await CRUD.create_user(session, user_model)


@router.put("/{user_id}", response_model=UserSchema)
async def update_user_full(
    user_id: str,
    user: UserUpdateFullSchema,
    session: AsyncSession = Depends(database.get_session),
):
    user_model = await CRUD.get_user(session, UUID(user_id))
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    return await CRUD.update_user(
        session,
        user_model,
        username=user.username,
        email=user.email,
        password=user.password,
    )


@router.patch("/{user_id}", response_model=UserSchema)
async def user_update_partial(
    user_id: str,
    user: UserUpdatePartialSchema,
    session: AsyncSession = Depends(database.get_session),
):
    user_model = await CRUD.get_user(session, UUID(user_id))
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    if all(field is None for field in user.model_dump().values()):
        raise HTTPException(status_code=400, detail="No fields to update")

    return await CRUD.update_user(
        session,
        user_model,
        username=user.username,
        email=user.email,
        password=user.password,
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: str, session: AsyncSession = Depends(database.get_session)
):
    user_model = await CRUD.get_user(session, UUID(user_id))
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    await CRUD.delete_user(session, user_model)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

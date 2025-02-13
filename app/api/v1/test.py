from fastapi import APIRouter, Depends

from app.db import database, AsyncSession
from app.db.user import User
from app.schemas import User as UserSchema

router = APIRouter()


@router.get("/")
async def read_root():
    return {"response": "This is a root of API v1"}


@router.get("/create/{username}")
async def test(username: str, session: AsyncSession = Depends(database.get_session)):
    user = User(
        username=username, email=f"{username}@test.com", password=f"pwd{username}"
    )
    session.add(user)
    await session.commit()

    return {"response": str(user.id)}


@router.get("/test2/{user_id}/", response_model=UserSchema)
async def test2(user_id: str, session: AsyncSession = Depends(database.get_session)):
    from uuid import UUID

    try:
        user = await session.get(User, UUID(user_id))
    except ValueError:
        return {"response": "Invalid user id"}

    if not user:
        return {"response": "User not found"}
    user.username = "different user"
    await session.commit()

    return user

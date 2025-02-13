from fastapi import APIRouter

from .users.routes import router as users_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["users"])


@router.get("/")
async def read_root():
    return {"response": "This is a root of API v1"}

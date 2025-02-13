from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.pydantic import partial_model


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    password: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


class UserUpdateFullSchema(BaseModel):
    username: str
    email: str
    password: str


@partial_model
class UserUpdatePartialSchema(BaseModel):
    username: str
    email: str
    password: str

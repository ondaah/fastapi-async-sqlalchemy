from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    password: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

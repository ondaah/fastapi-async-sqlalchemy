from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class User(BaseModel):
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

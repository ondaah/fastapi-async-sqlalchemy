from uuid import UUID, uuid4
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from app.core import settings
from app.utils.time import utcnow


class BaseModel(DeclarativeBase):
    """Abstract declarative base class for all database models.

    It provides `id`, `created_at` and `updated_at` fields out of the box.
    `id` is a UUID primary key. `created_at` and `updated_at` are datetime fields.
    """

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class Database:
    """Database utility class for managing database sessions and engine asynchronously."""

    def __init__(self) -> None:
        self.engine = create_async_engine(settings.db_url)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a new database session asynchronously."""
        async with self.session_factory() as session:
            yield session


database = Database()

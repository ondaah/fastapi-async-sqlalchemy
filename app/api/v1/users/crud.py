from uuid import UUID
from typing import Optional

from sqlalchemy import select

from app.db import AsyncSession, User


class CRUD:
    @classmethod
    async def get_users(cls, session: AsyncSession) -> list[User]:
        """Get all users.

        :param session: database session
        :type session: AsyncSession

        :return: list of users
        """
        result = await session.scalars(select(User))
        return list(result.all())

    @classmethod
    async def get_user(cls, session: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get user by id.

        :param session: database session
        :type session: AsyncSession
        :param user_id: target user id
        :type user_id: UUID

        :return: user if found, else None
        """
        return await session.get(User, user_id)

    @classmethod
    async def create_user(cls, session: AsyncSession, user: User) -> User:
        """Create user.

        :param session: database session
        :type session: AsyncSession
        :param user: user to create
        :type user: User

        :return: created user
        """
        session.add(user)
        await session.commit()
        return user

    @classmethod
    async def update_user(
        cls,
        session: AsyncSession,
        user: User,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> User:
        """Update user.

        :param session: database session
        :type session: AsyncSession
        :param user: user to update
        :type user: User

        :return: updated user
        """
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            user.password = password
        await session.commit()
        return user

    @classmethod
    async def delete_user_by_id(cls, session: AsyncSession, user_id: UUID) -> None:
        """Delete user by id.

        :param session: database session
        :type session: AsyncSession
        :param user_id: target user id
        :type user_id: UUID
        """
        user = await session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        await session.delete(user)
        await session.commit()

    @classmethod
    async def delete_user(cls, session: AsyncSession, user: User) -> None:
        """Delete user.

        :param session: database session
        :type session: AsyncSession
        :param user_id: target user id
        :type user_id: UUID
        """
        await session.delete(user)
        await session.commit()

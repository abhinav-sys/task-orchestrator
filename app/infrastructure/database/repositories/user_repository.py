"""User repository implementation."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.application.interfaces.user_repository import IUserRepository
from app.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    """User repository implementation."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository."""
        self.session = session

    async def create(self, user: User) -> User:
        """Create a new user."""
        user_model = UserModel(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return self._to_entity(user_model)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    async def update(self, user: User) -> User:
        """Update user."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one_or_none()
        if not user_model:
            raise ValueError(f"User with ID {user.id} not found")

        user_model.email = user.email
        user_model.username = user.username
        user_model.hashed_password = user.hashed_password
        user_model.full_name = user.full_name
        user_model.is_active = user.is_active
        user_model.is_superuser = user.is_superuser
        user_model.role = user.role
        user_model.updated_at = user.updated_at

        await self.session.commit()
        await self.session.refresh(user_model)
        return self._to_entity(user_model)

    async def delete(self, user_id: UUID) -> bool:
        """Delete user."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        if not user_model:
            return False

        await self.session.delete(user_model)
        await self.session.commit()
        return True

    def _to_entity(self, user_model: UserModel) -> User:
        """Convert model to entity."""
        return User(
            id=user_model.id,
            email=user_model.email,
            username=user_model.username,
            hashed_password=user_model.hashed_password,
            full_name=user_model.full_name,
            is_active=user_model.is_active,
            is_superuser=user_model.is_superuser,
            role=user_model.role,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )



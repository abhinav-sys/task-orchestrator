"""User repository interface."""

from typing import Optional
from uuid import UUID

from app.domain.entities.user import User


class IUserRepository:
    """User repository interface."""

    async def create(self, user: User) -> User:
        """Create a new user."""
        raise NotImplementedError

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        raise NotImplementedError

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        raise NotImplementedError

    async def update(self, user: User) -> User:
        """Update user."""
        raise NotImplementedError

    async def delete(self, user_id: UUID) -> bool:
        """Delete user."""
        raise NotImplementedError


"""User service."""

from typing import Optional
from uuid import UUID

from app.domain.entities.user import User
from app.domain.exceptions.domain_exceptions import UserNotFoundError
from app.application.dto.user_dto import UserUpdateDTO, UserResponseDTO
from app.application.interfaces.user_repository import IUserRepository


class UserService:
    """User service."""

    def __init__(self, user_repository: IUserRepository) -> None:
        """Initialize user service."""
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: UUID) -> UserResponseDTO:
        """Get user by ID."""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")

        return UserResponseDTO.model_validate(user)

    async def update_user(
        self, user_id: UUID, user_data: UserUpdateDTO
    ) -> UserResponseDTO:
        """Update user."""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")

        # Update fields
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        updated_user = await self.user_repository.update(user)
        return UserResponseDTO.model_validate(updated_user)

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete user."""
        return await self.user_repository.delete(user_id)



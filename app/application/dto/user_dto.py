"""User DTOs."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    """DTO for creating a user."""

    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserUpdateDTO(BaseModel):
    """DTO for updating a user."""

    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponseDTO(BaseModel):
    """DTO for user response."""

    id: UUID
    email: EmailStr
    username: str
    full_name: Optional[str]
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class UserLoginDTO(BaseModel):
    """DTO for user login."""

    email: EmailStr
    password: str


class TokenResponseDTO(BaseModel):
    """DTO for token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"



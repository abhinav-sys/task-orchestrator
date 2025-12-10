"""User entity."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """User domain entity."""

    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    role: str = Field(default="user")  # user, admin
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""

        from_attributes = True
        json_encoders = {UUID: str, datetime: lambda v: v.isoformat()}

    def __repr__(self) -> str:
        """String representation."""
        return f"<User {self.email}>"


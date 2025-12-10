"""JWT token handling."""

from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt

from app.config import settings


class JWTHandler:
    """JWT handler."""

    @staticmethod
    def create_access_token(user_id: UUID, email: str) -> str:
        """Create access token."""
        expire = datetime.utcnow() + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(
            payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def create_refresh_token(user_id: UUID, email: str) -> str:
        """Create refresh token."""
        expire = datetime.utcnow() + timedelta(
            days=settings.jwt_refresh_token_expire_days
        )
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(
            payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode JWT token."""
        return jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )


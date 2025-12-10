"""Authentication service."""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt

from app.config import settings
from app.domain.entities.user import User
from app.domain.exceptions.domain_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.application.dto.user_dto import (
    UserCreateDTO,
    UserLoginDTO,
    TokenResponseDTO,
)
from app.application.interfaces.user_repository import IUserRepository
from app.infrastructure.security.password_handler import PasswordHandler


class AuthService:
    """Authentication service."""

    def __init__(
        self,
        user_repository: IUserRepository,
        password_handler: PasswordHandler,
    ) -> None:
        """Initialize auth service."""
        self.user_repository = user_repository
        self.password_handler = password_handler

    async def signup(self, user_data: UserCreateDTO) -> User:
        """Sign up a new user."""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {user_data.email} already exists")

        existing_username = await self.user_repository.get_by_username(user_data.username)
        if existing_username:
            raise UserAlreadyExistsError(
                f"User with username {user_data.username} already exists"
            )

        # Hash password
        hashed_password = self.password_handler.hash_password(user_data.password)

        # Create user
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

        return await self.user_repository.create(user)

    async def login(self, login_data: UserLoginDTO) -> TokenResponseDTO:
        """Login user and return tokens."""
        # Get user by email
        user = await self.user_repository.get_by_email(login_data.email)
        if not user:
            raise InvalidCredentialsError("Invalid email or password")

        # Verify password
        if not self.password_handler.verify_password(
            login_data.password, user.hashed_password
        ):
            raise InvalidCredentialsError("Invalid email or password")

        # Check if user is active
        if not user.is_active:
            raise InvalidCredentialsError("User account is inactive")

        # Generate tokens
        access_token = self._create_access_token(user.id, user.email)
        refresh_token = self._create_refresh_token(user.id, user.email)

        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def get_current_user(self, token: str) -> User:
        """Get current user from token."""
        try:
            payload = jwt.decode(
                token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
            )
            user_id: UUID = UUID(payload.get("sub"))
            if user_id is None:
                raise InvalidCredentialsError("Invalid token")
        except (JWTError, ValueError) as e:
            raise InvalidCredentialsError(f"Invalid token: {str(e)}")

        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError("User not found")

        return user

    def _create_access_token(self, user_id: UUID, email: str) -> str:
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
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def _create_refresh_token(self, user_id: UUID, email: str) -> str:
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
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


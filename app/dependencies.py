"""Dependency injection."""

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.base import get_db
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.infrastructure.database.repositories.task_repository import TaskRepository
from app.application.services.auth_service import AuthService
from app.application.services.user_service import UserService
from app.application.services.task_service import TaskService
from app.infrastructure.security.password_handler import PasswordHandler


async def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[UserRepository, None]:
    """Get user repository."""
    yield UserRepository(session)


async def get_task_repository(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[TaskRepository, None]:
    """Get task repository."""
    yield TaskRepository(session)


def get_password_handler() -> PasswordHandler:
    """Get password handler."""
    return PasswordHandler()


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    password_handler: PasswordHandler = Depends(get_password_handler),
) -> AuthService:
    """Get auth service."""
    return AuthService(user_repo, password_handler)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Get user service."""
    return UserService(user_repo)


def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    """Get task service."""
    return TaskService(task_repo)


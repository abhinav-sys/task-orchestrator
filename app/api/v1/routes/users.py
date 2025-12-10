"""User routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.user_dto import UserResponseDTO, UserUpdateDTO
from app.application.services.user_service import UserService
from app.dependencies import get_user_service
from app.api.v1.routes.auth import get_current_user
from app.domain.entities.user import User
from app.domain.exceptions.domain_exceptions import UserNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponseDTO)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """Get current user profile."""
    return await user_service.get_user_by_id(current_user.id)


@router.put("/me", response_model=UserResponseDTO)
async def update_my_profile(
    user_data: UserUpdateDTO,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """Update current user profile."""
    try:
        return await user_service.update_user(current_user.id, user_data)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.application.dto.user_dto import (
    UserCreateDTO,
    UserLoginDTO,
    UserResponseDTO,
    TokenResponseDTO,
)
from app.application.services.auth_service import AuthService
from app.dependencies import get_auth_service
from app.domain.entities.user import User
from app.domain.exceptions.domain_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Get current authenticated user."""
    try:
        return await auth_service.get_current_user(token)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/signup", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreateDTO,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Sign up a new user."""
    try:
        user = await auth_service.signup(user_data)
        return UserResponseDTO.model_validate(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponseDTO)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Login user and get access token."""
    login_data = UserLoginDTO(email=form_data.username, password=form_data.password)
    try:
        return await auth_service.login(login_data)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponseDTO)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponseDTO.model_validate(current_user)



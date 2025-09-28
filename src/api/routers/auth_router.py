from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, status

from src.api.auth.security import create_access_token
from src.api.dependencies.database import get_user_repository
from src.core.application.use_cases.user import (
    AuthenticateUserInputDTO,
    AuthenticateUserUseCase,
    InvalidPasswordError,
    UserNotFoundError,
)
from src.core.infrastructure.config.settings import settings
from src.core.infrastructure.repositories import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
)
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    repository: UserRepository = Depends(get_user_repository),
):
    """
    Create JWT token for user.
    """

    use_case = AuthenticateUserUseCase(repository)
    input_dto = AuthenticateUserInputDTO(
        username=username,
        password=password,
    )

    try:
        user = use_case.execute(input_dto)
    except (UserNotFoundError, InvalidPasswordError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

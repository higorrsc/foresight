from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repository: UserRepository = Depends(get_user_repository),
):
    """
    Create JWT token for user.
    """

    use_case = AuthenticateUserUseCase(repository)
    input_dto = AuthenticateUserInputDTO(
        username=form_data.username,
        password=form_data.password,
    )

    try:
        user = use_case.execute(input_dto)
    except (UserNotFoundError, InvalidPasswordError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

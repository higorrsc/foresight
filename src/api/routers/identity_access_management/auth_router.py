from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status

from src.api.auth.security import create_access_token
from src.api.dependencies import get_user_repository
from src.core.infrastructure.config import settings
from src.identity_access_management.application.use_cases.user.commands import (
    AuthenticateUserInputDTO,
    AuthenticateUserUseCase,
)
from src.identity_access_management.domain.exceptions import (
    InvalidPasswordError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import IUserRepository

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
)
async def login_for_access_token(
    repo: Annotated[IUserRepository, Depends(get_user_repository)],
    username: str = Form(...),
    password: str = Form(...),
):
    """
    Create JWT token for user.
    """

    use_case = AuthenticateUserUseCase(repo)
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

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username},
        tenant_id=user.tenant_id,
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

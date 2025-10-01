from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.database import get_role_repository, get_user_repository
from src.api.routers.dto import PaginationMetaResponse
from src.core.application._shared.use_cases import (
    DeleteRequestInputDTO,
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)
from src.core.application.use_cases.user import (
    ChangePasswordInputDTO,
    ChangePasswordUseCase,
    CreateUserInputDTO,
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserByIdUseCase,
    InvalidPasswordError,
    ListUserUseCase,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)
from src.core.infrastructure.repositories import UserRepository
from src.core.infrastructure.repositories.role_repository import RoleRepository


class UserResponse(BaseModel):
    """
    Class that represents a user response.
    """

    id: UUID
    username: str


class PaginatedUserResponse(BaseModel):
    """
    Response model for API.
    """

    data: List[UserResponse]
    meta: PaginationMetaResponse


class ChangePasswordBody(BaseModel):
    """
    Request model for change password.
    """

    old_password: str
    new_password: str = Field(..., min_length=8)


public_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

protected_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@public_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def create_user_endpoint(
    request: CreateUserInputDTO,
    user_repo: UserRepository = Depends(get_user_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
):
    """
    Create a new user.
    """

    try:
        use_case = CreateUserUseCase(
            user_repo,
            role_repo,
        )
        result = use_case.execute(request)
        return result
    except UsernameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@protected_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedUserResponse,
)
def list_users_endpoint(
    repo: UserRepository = Depends(get_user_repository),
    username: str = Query(None, description="Filtrar por parte do username"),
    sort_by: str = Query("username", description="Campo para ordenação"),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """
    List users with filters, order and pagination.
    """

    filters = {"username": username} if username else {}
    input_dto = ListRequestInputDTO(
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )
    use_case = ListUserUseCase(repository=repo)
    result = use_case.execute(input_dto)

    return result


@protected_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def get_user_by_id_endpoint(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
):
    """
    Getting an user by its ID.
    """

    try:
        use_case = GetUserByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=user_id)
        user = use_case.execute(input_dto)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@protected_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_endpoint(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
):
    """
    Delete an existing user.
    """

    try:
        use_case = DeleteUserUseCase(repository=repo)
        use_case.execute(DeleteRequestInputDTO(id=user_id))
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@protected_router.patch("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password_endpoint(
    user_id: UUID,
    request_body: ChangePasswordBody,
    repo: UserRepository = Depends(get_user_repository),
):
    """
    Change the password of an existing user.
    """

    try:
        use_case = ChangePasswordUseCase(repository=repo)
        input_dto = ChangePasswordInputDTO(
            user_id=user_id,
            old_password=request_body.old_password,
            new_password=request_body.new_password,
        )
        use_case.execute(input_dto)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

from src.identity_access_management.application.use_cases.user import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.repositories import IUserRepository
from src.shared_kernel.application._shared.use_cases.queries import ListRequestInputDTO
from src.shared_kernel.domain._shared.repository import PaginatedResult


class ListUserUseCase:
    """
    Use case to list users.
    """

    def __init__(self, repository: IUserRepository) -> None:
        """
        Initialize the ListUserUseCase.

        :param repository: The repository to use for listing users.
        """

        self._repository = repository

    def execute(self, input_dto: ListRequestInputDTO) -> PaginatedResult[User]:
        """
        Execute the ListUserUseCase.

        :param input_dto: The input data transfer object.
        :return: A list of users.
        """

        if AppPermission.USER_READ not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to list users."
            )

        paginated_result = self._repository.search(
            tenant_id=input_dto.actor.tenant_id,
            filters=input_dto.filters,
            sort_by=input_dto.sort_by,
            sort_order=input_dto.sort_order,  # type: ignore
            offset=input_dto.offset,
            limit=input_dto.limit,
            include_inactive=input_dto.include_inactive,
        )

        return PaginatedResult(
            data=paginated_result.data,
            total=paginated_result.total,
        )

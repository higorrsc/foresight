from dataclasses import dataclass, field
from math import ceil
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from src.core.application import PaginatedResponseDTO, PaginationMeta
from src.core.domain import AbstractRepository
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User

T = TypeVar("T")


@dataclass
class ListRequestInputDTO:
    """
    Data Transfer Object for list requests.
    """

    actor: "User"
    filters: dict[str, Any] | None = field(default_factory=dict)
    sort_by: str | None = None
    sort_order: str | None = "asc"
    offset: int = 0
    limit: int = 10
    include_inactive: bool = False


class GenericListUseCase(Generic[T]):
    """
    Use case for listing entities of type T.
    """

    def __init__(self, repository: AbstractRepository[T]) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing entities.
        """

        self._repository = repository

    def execute(self, input_dto: ListRequestInputDTO) -> PaginatedResponseDTO[T]:
        """
        Execute the list use case.

        :return: A list of entities.
        """

        if AppPermission.USER_READ not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to list data."
            )

        repo_result = self._repository.search(
            tenant_id=input_dto.actor.tenant_id,
            filters=input_dto.filters,
            sort_by=input_dto.sort_by,
            sort_order=input_dto.sort_order,  # type: ignore
            offset=input_dto.offset,
            limit=input_dto.limit,
            include_inactive=input_dto.include_inactive,
        )

        total_items = repo_result.total
        page_size = input_dto.limit

        total_pages = ceil(total_items / page_size) if page_size > 0 else 0
        current_page = (input_dto.offset // page_size) + 1 if page_size > 0 else 1

        meta = PaginationMeta(
            total_items=total_items,
            current_page=current_page,
            page_size=page_size,
            total_pages=total_pages,
        )

        return PaginatedResponseDTO(data=repo_result.data, meta=meta)

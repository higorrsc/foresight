from dataclasses import dataclass, field
from math import ceil
from typing import Any, Dict, Generic, List, Optional, TypeVar

from src.core.domain._shared import AbstractRepository

T = TypeVar("T")


@dataclass
class ListRequestInputDTO:
    """
    Data Transfer Object for list requests.
    """

    filters: Optional[Dict[str, Any]] = field(default_factory=dict)
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"
    offset: int = 0
    limit: int = 10


@dataclass
class PaginationMeta:
    """
    Metadata for pagination.
    """

    total_items: int
    current_page: int
    page_size: int
    total_pages: int


@dataclass(frozen=True)
class ListResponseOutputDTO(Generic[T]):
    """
    Data Transfer Object for list requests.
    """

    data: List[T]
    meta: PaginationMeta


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

    def execute(self, input_dto: ListRequestInputDTO) -> ListResponseOutputDTO[T]:
        """
        Execute the list use case.

        :return: A list of entities.
        """

        repo_result = self._repository.search(
            filters=input_dto.filters,
            sort_by=input_dto.sort_by,
            sort_order=input_dto.sort_order,  # type: ignore
            offset=input_dto.offset,
            limit=input_dto.limit,
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

        return ListResponseOutputDTO(data=repo_result.data, meta=meta)

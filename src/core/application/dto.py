from dataclasses import dataclass


@dataclass(frozen=True)
class PaginationMeta:
    """
    Calculated metadata for pagination.
    """

    total_items: int
    current_page: int
    page_size: int
    total_pages: int


@dataclass(frozen=True)
class PaginatedResponseDTO[T]:
    """
    DTO that represents a paginated response.
    """

    data: list[T]
    meta: PaginationMeta

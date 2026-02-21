from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class PaginationMetaResponse(BaseModel):
    """
    Response meta for API.
    """

    total_items: int
    current_page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedApiResponse(BaseModel, Generic[T]):
    """
    Response model for API.
    """

    data: list[T]
    meta: PaginationMetaResponse

    model_config = ConfigDict(from_attributes=True)

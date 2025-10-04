from pydantic import BaseModel


class PaginationMetaResponse(BaseModel):
    """
    Metadata for pagination.
    """

    total_items: int
    current_page: int
    page_size: int
    total_pages: int

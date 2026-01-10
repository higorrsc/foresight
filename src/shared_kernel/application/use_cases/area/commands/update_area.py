from src.core.application.use_cases.commands import UpdateDescribedEntityUseCase
from src.shared_kernel.application.use_cases.area import (
    AreaNotFoundError,
    InvalidAreaError,
)
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.repositories import IAreaRepository


class UpdateAreaUseCase(UpdateDescribedEntityUseCase[Area]):
    """
    Use case for updating an existing area.
    """

    def __init__(self, repository: IAreaRepository) -> None:
        """
        Initialize the UpdateAreaUseCase.
        """

        super().__init__(
            repository,
            AreaNotFoundError,
            InvalidAreaError,
        )

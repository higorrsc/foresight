from src.shared_kernel.application._shared.use_cases.commands import (
    UpdateDescribedEntityUseCase,
)
from src.shared_kernel.application.use_cases.area import (
    AreaNotFoundError,
    InvalidAreaError,
)
from src.shared_kernel.domain._shared import AbstractRepository
from src.shared_kernel.domain.entities import Area


class UpdateAreaUseCase(UpdateDescribedEntityUseCase[Area]):
    """
    Use case for updating an existing area.
    """

    def __init__(self, repository: AbstractRepository[Area]) -> None:
        """
        Initialize the UpdateAreaUseCase.
        """

        super().__init__(
            repository,
            AreaNotFoundError,
            InvalidAreaError,
        )

from src.core.application._shared.use_cases import UpdateDescribedEntityUseCase
from src.core.application.use_cases.area import AreaNotFoundError, InvalidAreaError
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Area


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

from src.core.application._shared.use_cases.commands import CreateDescribedEntityUseCase
from src.core.application.use_cases.area import InvalidAreaError
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Area


class CreateAreaUseCase(CreateDescribedEntityUseCase[Area]):
    """
    Create a new area.
    """

    def __init__(self, repository: AbstractRepository[Area]) -> None:
        """
        Initialize the CreateAreaUseCase.
        """

        super().__init__(
            repository,
            Area,
            InvalidAreaError,
        )

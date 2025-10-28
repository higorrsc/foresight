from src.shared_kernel.application._shared.use_cases.commands import (
    CreateDescribedEntityUseCase,
)
from src.shared_kernel.application.use_cases.area import InvalidAreaError
from src.shared_kernel.domain._shared import AbstractRepository
from src.shared_kernel.domain.entities.area import Area


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

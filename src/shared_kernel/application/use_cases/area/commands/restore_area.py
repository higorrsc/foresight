from src.shared_kernel.application._shared.use_cases.commands import (
    GenericRestoreUseCase,
)
from src.shared_kernel.application.use_cases.area import AreaNotFoundError
from src.shared_kernel.domain._shared import AbstractRepository
from src.shared_kernel.domain.entities import Area


class RestoreAreaUseCase(GenericRestoreUseCase[Area]):
    """
    Use case for deleting an area.
    """

    def __init__(self, repository: AbstractRepository[Area]) -> None:
        """
        Initialize the restore use case.
        """

        super().__init__(
            repository,
            AreaNotFoundError,
            "Area with given ID not found.",
        )

from src.core.application._shared.use_cases.commands import GenericRestoreUseCase
from src.core.application.use_cases.area import AreaNotFoundError
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Area


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

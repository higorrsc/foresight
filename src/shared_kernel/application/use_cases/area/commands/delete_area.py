from src.shared_kernel.application._shared.use_cases.commands import (
    GenericDeleteUseCase,
)
from src.shared_kernel.application.use_cases.area import AreaNotFoundError
from src.shared_kernel.domain._shared import AbstractRepository
from src.shared_kernel.domain.entities import Area


class DeleteAreaUseCase(GenericDeleteUseCase[Area]):
    """
    Use case for deleting an area.
    """

    def __init__(self, repository: AbstractRepository[Area]) -> None:
        """
        Initialize the delete use case.
        """

        super().__init__(
            repository,
            AreaNotFoundError,
            "Area with given ID not found.",
        )

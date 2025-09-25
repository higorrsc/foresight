from core.application._shared.use_cases import GenericDeleteUseCase
from core.application.use_cases.area import AreaNotFoundError
from core.domain._shared.repository import AbstractRepository
from core.domain.entities.area import Area


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

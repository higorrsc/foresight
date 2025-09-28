from src.core.application._shared.use_cases import GenericGetByIdUseCase
from src.core.application.use_cases.area import AreaNotFoundError
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Area


class GetAreaByIdUseCase(GenericGetByIdUseCase[Area]):
    """
    Use case for getting an area by its ID.
    """

    def __init__(self, repository: AbstractRepository[Area]) -> None:
        """
        Initialize the get by id use case.
        """

        super().__init__(
            repository,
            AreaNotFoundError,
            "Area with given ID not found.",
        )

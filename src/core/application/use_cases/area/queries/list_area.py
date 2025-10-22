from src.core.application._shared.use_cases.queries import GenericListUseCase
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Area


class ListAreaUseCase(GenericListUseCase[Area]):
    """
    Use case for listing areas.
    """

    def __init__(self, repository: AbstractRepository[Area]) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing areas.
        """

        super().__init__(repository)

from core.application._shared.use_cases import GenericListUseCase
from core.domain._shared.repository import AbstractRepository
from core.domain.entities.area import Area


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

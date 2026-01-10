from src.core.application.use_cases.queries import GenericGetByIdUseCase
from src.shared_kernel.application.use_cases.area import AreaNotFoundError
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.repositories import IAreaRepository


class GetAreaByIdUseCase(GenericGetByIdUseCase[Area]):
    """
    Use case for getting an area by its ID.
    """

    def __init__(self, repository: IAreaRepository) -> None:
        """
        Initialize the get by id use case.
        """

        super().__init__(
            repository,
            AreaNotFoundError,
            "Area with given ID not found.",
        )

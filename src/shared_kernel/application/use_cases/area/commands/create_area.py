from src.core.application.use_cases.commands import CreateDescribedEntityUseCase
from src.shared_kernel.application.use_cases.area import InvalidAreaError
from src.shared_kernel.domain.entities.area import Area
from src.shared_kernel.domain.repositories import IAreaRepository


class CreateAreaUseCase(CreateDescribedEntityUseCase[Area]):
    """
    Create a new area.
    """

    def __init__(self, repository: IAreaRepository) -> None:
        """
        Initialize the CreateAreaUseCase.
        """

        super().__init__(
            repository,
            Area,
            InvalidAreaError,
        )

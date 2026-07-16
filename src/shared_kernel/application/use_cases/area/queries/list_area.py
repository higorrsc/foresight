from src.core.application.use_cases.queries import GenericListUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.repositories import IAreaRepository


class ListAreaUseCase(GenericListUseCase[Area]):
    """
    Use case for listing areas.
    """

    def __init__(self, repository: IAreaRepository) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing areas.
        """

        super().__init__(
            repository,
            AppPermission.AREA_READ,
        )

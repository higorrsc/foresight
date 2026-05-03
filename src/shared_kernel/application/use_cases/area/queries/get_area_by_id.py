from src.core.application.use_cases.queries import GenericGetByIdUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.exceptions import AreaNotFoundError
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
            AppPermission.AREA_READ,
            AreaNotFoundError,
            "Area with given ID not found.",
        )

from src.core.application.use_cases.commands import UpdateDescribedEntityUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.exceptions import AreaNotFoundError, InvalidAreaError
from src.shared_kernel.domain.repositories import IAreaRepository


class UpdateAreaUseCase(UpdateDescribedEntityUseCase[Area]):
    """
    Use case for updating an existing area.
    """

    def __init__(self, repository: IAreaRepository) -> None:
        """
        Initialize the UpdateAreaUseCase.
        """

        super().__init__(
            repository,
            AppPermission.AREA_UPDATE,
            AreaNotFoundError,
            InvalidAreaError,
        )

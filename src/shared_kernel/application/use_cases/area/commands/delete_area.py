from src.core.application.use_cases.commands import GenericDeleteUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.exceptions import AreaNotFoundError
from src.shared_kernel.domain.repositories import IAreaRepository


class DeleteAreaUseCase(GenericDeleteUseCase[Area]):
    """
    Use case for deleting an area.
    """

    def __init__(self, repository: IAreaRepository) -> None:
        """
        Initialize the delete use case.
        """

        super().__init__(
            repository,
            AppPermission.AREA_DELETE,
            AreaNotFoundError,
            "Area with given ID not found.",
        )

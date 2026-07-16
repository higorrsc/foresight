from src.core.application.use_cases.commands import GenericDeleteUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.exceptions import OrganizationalUnitNotFoundError
from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository


class DeleteOrganizationalUnitUseCase(GenericDeleteUseCase[OrganizationalUnit]):
    """
    Use case for deleting an organizational unit.
    """

    def __init__(self, repository: IOrganizationalUnitRepository) -> None:
        """
        Initialize the DeleteOrganizationalUnitUseCase.
        """

        super().__init__(
            repository,
            AppPermission.ORGANIZATIONAL_UNIT_DELETE,
            OrganizationalUnitNotFoundError,
            "Organizational Unit with given ID not found.",
        )

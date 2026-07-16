from src.core.application.use_cases.queries import GenericListUseCase
from src.identity_access_management.domain.constants.permissions import AppPermission
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository


class ListOrganizationalUnitUseCase(GenericListUseCase[OrganizationalUnit]):
    """
    Use case for listing organizaOrganizationalUnits.
    """

    def __init__(self, repository: IOrganizationalUnitRepository) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing organizational units.
        """

        super().__init__(
            repository,
            AppPermission.ORGANIZATIONAL_UNIT_READ,
        )

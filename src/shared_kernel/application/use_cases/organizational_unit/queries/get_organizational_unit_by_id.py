from src.core.application.use_cases.queries import GenericGetByIdUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.exceptions import OrganizationalUnitNotFoundError
from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository


class GetOrganizationalUnitByIdUseCase(GenericGetByIdUseCase[OrganizationalUnit]):
    """
    Use case for getting an organizational unit by its ID.
    """

    def __init__(self, repository: IOrganizationalUnitRepository) -> None:
        """
        Initialize the get by id use case.
        """

        super().__init__(
            repository,
            AppPermission.ORGANIZATIONAL_UNIT_READ,
            OrganizationalUnitNotFoundError,
            "Organizational Unit with given ID not found.",
        )

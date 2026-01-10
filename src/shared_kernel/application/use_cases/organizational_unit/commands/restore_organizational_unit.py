from src.core.application.use_cases.commands import GenericRestoreUseCase
from src.shared_kernel.application.use_cases.organizational_unit import (
    OrganizationalUnitNotFoundError,
)
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository


class RestoreOrganizationalUnitUseCase(GenericRestoreUseCase[OrganizationalUnit]):
    """
    Use case for deleting an organizational unit.
    """

    def __init__(self, repository: IOrganizationalUnitRepository) -> None:
        """
        Initialize the RestoreOrganizationalUnitUseCase.
        """

        super().__init__(
            repository,
            OrganizationalUnitNotFoundError,
            "Organizational Unit with given ID not found.",
        )

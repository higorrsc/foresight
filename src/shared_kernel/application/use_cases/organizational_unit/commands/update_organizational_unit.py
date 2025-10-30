from src.shared_kernel.application._shared.use_cases.commands import (
    UpdateDescribedEntityUseCase,
)
from src.shared_kernel.application.use_cases.organizational_unit import (
    InvalidOrganizationalUnitError,
    OrganizationalUnitNotFoundError,
)
from src.shared_kernel.domain._shared import AbstractRepository
from src.shared_kernel.domain.entities import OrganizationalUnit


class UpdateOrganizationalUnitUseCase(UpdateDescribedEntityUseCase[OrganizationalUnit]):
    """
    Use case for updating an existing organizational unit.
    """

    def __init__(self, repository: AbstractRepository[OrganizationalUnit]) -> None:
        """
        Initialize the UpdateOrganizationalUnitUseCase.
        """

        super().__init__(
            repository,
            OrganizationalUnitNotFoundError,
            InvalidOrganizationalUnitError,
        )

from src.shared_kernel.application._shared.use_cases.commands import (
    CreateDescribedEntityUseCase,
)
from src.shared_kernel.application.use_cases.organizational_unit import (
    InvalidOrganizationalUnitError,
)
from src.shared_kernel.domain._shared import AbstractRepository
from src.shared_kernel.domain.entities import OrganizationalUnit


class CreateOrganizationalUnitUseCase(CreateDescribedEntityUseCase[OrganizationalUnit]):
    """
    Create a new organizationalUnit.
    """

    def __init__(self, repository: AbstractRepository[OrganizationalUnit]) -> None:
        """
        Initialize the CreateOrganizationalUnitUseCase.
        """

        super().__init__(
            repository,
            OrganizationalUnit,
            InvalidOrganizationalUnitError,
        )

from src.shared_kernel.application._shared.use_cases.queries import GenericListUseCase
from src.shared_kernel.domain._shared import AbstractRepository
from src.shared_kernel.domain.entities import OrganizationalUnit


class ListOrganizationalUnitUseCase(GenericListUseCase[OrganizationalUnit]):
    """
    Use case for listing organizaOrganizationalUnits.
    """

    def __init__(self, repository: AbstractRepository[OrganizationalUnit]) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing organizational units.
        """

        super().__init__(repository)

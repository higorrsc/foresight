from abc import abstractmethod
from uuid import UUID

from src.core.domain import AbstractRepository
from src.identity_access_management.domain.entities import Role


class IRoleRepository(AbstractRepository[Role]):
    """
    Interface for the Role Repository.
    """

    @abstractmethod
    def get_by_name(
        self,
        name: str,
        tenant_id: UUID | None,
    ) -> Role | None:
        """
        Get a role by its name.
        """

        raise NotImplementedError  # pragma: no cover

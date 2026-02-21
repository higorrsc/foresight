from abc import abstractmethod

from src.core.domain.repository import AbstractRepository
from src.identity_access_management.domain.entities import Permission


class IPermissionRepository(AbstractRepository[Permission]):
    """
    Interface (contract) for the Permission repository.
    """

    @abstractmethod
    def list_all(self) -> list[Permission]:
        """
        Lists all permissions in the system.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_codename(self, codename: str) -> Permission | None:
        """
        Retrieves a permission by its codename.
        """

        raise NotImplementedError  # pragma: no cover

from abc import abstractmethod
from typing import List

from src.identity_access_management.domain.entities import Permission
from src.shared_kernel.domain._shared.repository import AbstractRepository


class IPermissionRepository(AbstractRepository[Permission]):
    """
    Interface (contract) for the Permission repository.
    """

    @abstractmethod
    def list_all(self) -> List[Permission]:
        """
        Lists all permissions in the system.
        """

        raise NotImplementedError  # pragma: no cover

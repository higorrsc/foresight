from abc import abstractmethod
from typing import Optional

from src.core.domain import AbstractRepository
from src.tenant_management.domain.entities import Plan


class IPlanRepository(AbstractRepository[Plan]):
    """
    Interface (contract) for the Plan repository.
    """

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Plan]:
        """
        Finds a plan by its unique name.
        """

        raise NotImplementedError  # pragma: no cover

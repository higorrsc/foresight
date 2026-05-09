from abc import abstractmethod

from src.core.domain import AbstractRepository
from src.tenant_management.domain.entities import Plan


class IPlanRepository(AbstractRepository[Plan]):
    """
    Interface (contract) for the Plan repository.
    """

    @abstractmethod
    async def get_by_name(self, name: str) -> Plan | None:
        """
        Finds a plan by its unique name.
        """

        raise NotImplementedError  # pragma: no cover

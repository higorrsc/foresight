from src.core.domain.repository import AbstractRepository
from src.shared_kernel.domain.entities import Area


class IAreaRepository(AbstractRepository[Area]):
    """
    Interface for the Area Repository.
    """

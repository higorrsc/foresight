from src.shared_kernel.domain._shared.repository import AbstractRepository
from src.shared_kernel.domain.entities.area import Area


class IAreaRepository(AbstractRepository[Area]):
    """
    Interface for the Area Repository.
    """

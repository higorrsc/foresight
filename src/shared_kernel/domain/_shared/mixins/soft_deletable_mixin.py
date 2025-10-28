from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class SoftDeletableMixin:
    """
    Mixin to add soft delete functionality to an entity.
    """

    is_active: bool = field(default=True, init=True)
    deleted_at: Optional[datetime] = field(default=None, init=False)

    def soft_delete(self) -> None:
        """
        Soft delete the entity.
        """

        self.is_active = False
        self.deleted_at = datetime.now()

    def restore(self) -> None:
        """
        Restore the entity.
        """

        self.is_active = True
        self.deleted_at = None

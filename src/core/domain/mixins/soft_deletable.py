from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(kw_only=True)
class SoftDeletableMixin:
    """
    Mixin to add soft delete functionality to an entity.
    """

    is_active: bool = field(default=True, init=True)
    deleted_at: datetime | None = field(default=None, init=False)

    def soft_delete(self) -> None:
        """
        Soft delete the entity.
        """

        self.is_active = False
        self.deleted_at = datetime.now(UTC)

    def restore(self) -> None:
        """
        Restore the entity.
        """

        self.is_active = True
        self.deleted_at = None

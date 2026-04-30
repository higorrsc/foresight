from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass(kw_only=True)
class UserAuditMixin:
    """
    Mixin to add user auditing functionality to an entity.
    """

    created_by: UUID | None = field(default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_by: UUID | None = field(default=None)
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def update_audit_info(self, user_id: UUID) -> None:
        """
        Update the updated_by field with the user ID.

        Args:
            user_id (UUID): The ID of the user performing the update.
        """
        self.updated_by = user_id
        self.updated_at = datetime.now(UTC)

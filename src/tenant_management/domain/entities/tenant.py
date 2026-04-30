from dataclasses import dataclass, field
from uuid import UUID

from src.core.domain.entities import AbstractEntity
from src.core.domain.exceptions import EntityValidationError
from src.core.domain.mixins import UserAuditMixin
from src.tenant_management.domain.value_objects import TenantStatus


@dataclass(kw_only=True, eq=False, repr=False)
class Tenant(AbstractEntity, UserAuditMixin):
    """
    Entity representing a Tenant in the system.
    """

    name: str
    status: TenantStatus = field(default=TenantStatus.TRIAL)
    plan_id: UUID

    def _str_fields(self) -> str:
        """
        Returns a string representation of the fields of the Tenant entity.
        """

        return f"id={self.id}, name='{self.name}'"

    def validate(self) -> None:
        """
        Validates the Tenant entity's attributes.
        """

        if not self.name or not self.name.strip():
            self.notification.add_error("Tenant name is required.")

        if self.name and len(self.name) > 100:
            self.notification.add_error("Tenant must be at most 100 characters long.")

        if not self.plan_id or not isinstance(self.plan_id, UUID):
            self.notification.add_error("Tenant plan_id must be a valid UUID.")

        if not self.status:
            self.notification.add_error("Tenant status is required.")

        if not isinstance(self.status, TenantStatus):
            self.notification.add_error("Tenant status must be a valid TenantStatus.")

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

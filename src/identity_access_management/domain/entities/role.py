from dataclasses import dataclass, field

from src.core.domain import EntityValidationError
from src.core.domain.entities import TenantAwareEntity
from src.core.domain.mixins import SoftDeletableMixin, UserAuditMixin


@dataclass(kw_only=True, eq=False, repr=False)
class Role(TenantAwareEntity, SoftDeletableMixin, UserAuditMixin):
    """
    Entity representing a role in the system.
    """

    name: str
    description: str
    permissions: set[str] = field(default_factory=set)

    def _str_fields(self) -> str:
        """
        Returns a string representation of the fields of the Role entity.
        """

        return f"id={self.id}, name='{self.name}'"

    def update_role(self, new_name: str, new_description: str | None = None) -> None:
        """
        Updates the name and description of the Role entity.
        """

        self.name = new_name
        self.description = new_description  # type: ignore
        self.validate()

    def validate(self) -> None:
        """
        Validates the Role entity's attributes.
        """

        if not self.name or not self.name.strip():
            self.notification.add_error("Role name is required.")

        if len(self.name) > 100:
            self.notification.add_error(
                "Role name must be at most 100 characters long."
            )

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

from dataclasses import dataclass, field
from typing import Optional, Set

from src.shared_kernel.domain._shared import EntityValidationError
from src.shared_kernel.domain._shared.entities import TenantAwareEntity


@dataclass(kw_only=True, eq=False)
class Role(TenantAwareEntity):
    """
    Entity representing a role in the system.
    """

    name: str
    description: str
    permissions: Set[str] = field(default_factory=set)

    def update_role(self, new_name: str, new_description: Optional[str] = None) -> None:
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

    def __str__(self) -> str:
        """
        Returns a string representation of the Role entity.
        """

        return f"Role(id={self.id}, name='{self.name}')"

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the Role entity.
        """

        return f"<Role {self.name} ({self.id})>"

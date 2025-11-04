from dataclasses import dataclass, field
from typing import Optional, Set
from uuid import UUID

from src.shared_kernel.domain._shared import EntityValidationError
from src.shared_kernel.domain._shared.entities import AbstractEntity


@dataclass(kw_only=True, eq=False)
class Role(AbstractEntity):
    """
    Entity representing a role in the system.
    """

    name: str
    description: str
    permissions: Set[str] = field(default_factory=set)
    tenant_id: UUID

    def update_role(self, new_name: str, new_description: Optional[str] = None) -> None:
        """
        Updates the name and description of the Role entity.
        """

        self.name = new_name
        self.description = new_description  # type: ignore
        self._validate()

    def _validate(self) -> None:
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

from dataclasses import dataclass
from typing import Optional

from src.core.domain._shared import AbstractEntity, EntityValidationError


@dataclass(kw_only=True, eq=False)
class Role(AbstractEntity):
    """
    Entity representing a role in the system.
    """

    name: str
    description: str

    def update_role(self, new_name: str, new_description: Optional[str] = None) -> None:
        """
        Updates the name and description of the Role entity.
        """

        self.name = new_name
        self.description = new_description  # type: ignore
        self._validate()

    def _validate(self) -> None:
        if not self.name or not self.name.strip():
            self.notification.add_error("Role name is required.")
        if len(self.name) > 100:
            self.notification.add_error(
                "Role name must be at most 100 characters long."
            )
        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

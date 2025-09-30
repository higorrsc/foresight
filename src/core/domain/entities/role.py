from dataclasses import dataclass

from src.core.domain._shared.entity import AbstractEntity
from src.core.domain._shared.exceptions import EntityValidationError


@dataclass(kw_only=True, eq=False)
class Role(AbstractEntity):
    """
    Entity representing a role in the system.
    """

    name: str
    description: str

    def _validate(self) -> None:
        if not self.name or not self.name.strip():
            self.notification.add_error("Role name is required.")
        if len(self.name) > 100:
            self.notification.add_error(
                "Role name must be at most 100 characters long."
            )
        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

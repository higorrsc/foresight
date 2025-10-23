from dataclasses import dataclass
from typing import Optional

from src.core.domain._shared.entities import AbstractEntity
from src.core.domain._shared.exceptions import EntityValidationError


@dataclass(kw_only=True, eq=False)
class Permission(AbstractEntity):
    """
    Entity representing a permission in the system.
    """

    codename: str
    description: str

    def update_permission(
        self,
        new_codename: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> None:
        """
        Updates the codename and description of the Permission entity.
        """

        if new_codename:
            self.codename = new_codename

        if new_description:
            self.description = new_description

        self._validate()

    def _validate(self) -> None:
        """
        Validates the Permission entity's attributes.
        """

        if not self.codename or not self.codename.strip():
            self.notification.add_error("Permission codename is required.")

        if len(self.codename) > 100:
            self.notification.add_error(
                "Permission codename must be at most 100 characters long."
            )

        if not self.description or not self.description.strip():
            self.notification.add_error("Permission description is required.")

        if len(self.description) > 200:
            self.notification.add_error(
                "Permission description must be at most 200 characters long."
            )

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

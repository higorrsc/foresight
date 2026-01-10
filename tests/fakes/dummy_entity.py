from dataclasses import dataclass

from src.core.domain.entities import TenantAwareEntity


@dataclass(kw_only=True, eq=False)
class DummyEntity(TenantAwareEntity):
    """
    A dummy entity for testing purposes.
    """

    name: str

    def validate(self):
        """
        Validate the entity.

        Raises:
            ValueError: If the entity is in an invalid state.
        """

        if not self.name:
            self.notification.add_error("Name cannot be empty")

        if not isinstance(self.name, str):
            self.notification.add_error("Name must be a string")

        if len(self.name) < 3:
            self.notification.add_error("Name must be at least 3 characters long")

        if len(self.name) > 255:
            self.notification.add_error("Name must be less than 255 characters long")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

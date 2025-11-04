from dataclasses import dataclass
from decimal import Decimal

from src.shared_kernel.domain._shared.entities import AbstractEntity
from src.shared_kernel.domain._shared.exceptions import EntityValidationError


@dataclass(kw_only=True, eq=False)
class Plan(AbstractEntity):
    """
    Entity representing a Plan in the system.
    """

    name: str
    price: Decimal

    def _validate(self) -> None:
        """
        Validates the Plan entity's attributes.
        """

        if not self.name or not self.name.strip():
            self.notification.add_error("Plan name is required.")

        if len(self.name) > 100:
            self.notification.add_error("Plan must be at most 100 characters long.")

        if not self.price or not isinstance(self.price, Decimal):
            self.notification.add_error("Plan price must be a valid Decimal.")

        if self.price <= 0:
            self.notification.add_error("Plan price must be greater than zero.")

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

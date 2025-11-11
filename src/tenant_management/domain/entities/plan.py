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

    def validate(self) -> None:
        """
        Validates the Plan entity's attributes.
        """

        if not self.name or not self.name.strip():
            self.notification.add_error("Plan name is required.")

        if self.name and len(self.name) > 100:
            self.notification.add_error("Plan must be at most 100 characters long.")

        if not self.price or not isinstance(self.price, Decimal):
            self.notification.add_error("Plan price must be a valid Decimal.")

        if isinstance(self.price, Decimal) and self.price <= 0:
            self.notification.add_error("Plan price must be greater than zero.")

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

    def __str__(self) -> str:
        """
        Returns a string representation of the Plan entity.
        """

        return f"Plan(id={self.id}, name='{self.name}')"

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the Plan entity.
        """

        return f"<Plan {self.name} ({self.id})>"

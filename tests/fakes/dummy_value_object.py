from dataclasses import dataclass
from decimal import Decimal

from src.shared_kernel.domain._shared import AbstractValueObject


@dataclass(kw_only=True)
class DummyValueObjectForMoneyType(AbstractValueObject):
    """
    A dummy value object for money type.
    """

    amount: Decimal
    currency: str

    def validate(self):
        """
        Validate the value object.

        Raises:
            ValueError: If the value object is in an invalid state.
        """

        if not self.amount:
            raise ValueError("Amount cannot be empty")
        if not isinstance(self.amount, Decimal):
            raise ValueError("Amount must be a decimal")
        if not self.currency:
            raise ValueError("Currency cannot be empty")
        if not isinstance(self.currency, str):
            raise ValueError("Currency must be a string")
        if len(self.currency) != 3:
            raise ValueError("Currency must be exactly 3 characters long")

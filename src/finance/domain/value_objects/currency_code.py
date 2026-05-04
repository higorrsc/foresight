from dataclasses import dataclass

from src.core.domain import AbstractValueObject, EntityValidationError
from src.finance.domain.constants import VALID_CURRENCY_CODES


@dataclass(frozen=True, kw_only=True)
class CurrencyCode(AbstractValueObject):
    """
    Value object representing a currency code.
    """

    value: str

    def __post_init__(self):
        """
        Validate the value object after initialization.
        """

        object.__setattr__(self, "value", self.value.upper())
        super().__post_init__()

    def __repr__(self) -> str:
        """
        Returns a string representation of the value object.
        """

        return f"<CurrencyCode value={self.value}>"

    def __str__(self) -> str:
        """
        Returns a string representation of the value object.

        Returns:
            str: A string representation of the value object.
        """

        return self.value

    def validate(self):
        """
        Validate the value object.

        This method should be implemented in the concrete subclasses to validate
        the value object's state. It should raise a EntityValidationError if the value
        object is in an invalid state.

        Raises:
            EntityValidationError: If the value object is in an invalid state.
        """

        if len(self.value) != 3:
            raise EntityValidationError("Currency code must be 3 characters long")

        if not self.value.isalpha():
            raise EntityValidationError("Currency code must contain only letters")

        if self.value not in VALID_CURRENCY_CODES:
            raise EntityValidationError(f"Invalid ISO 4217 currency code: {self.value}")

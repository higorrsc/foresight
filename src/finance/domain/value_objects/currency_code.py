from dataclasses import dataclass

from src.core.domain import AbstractValueObject
from src.finance.domain.entities.currency import currency_catalog


@dataclass(frozen=True, kw_only=True)
class CurrencyCode(AbstractValueObject):
    """
    ISO 4217 currency code value object.
    """

    value: str

    def __post_init__(self):
        """Validate and normalize the currency code."""

        normalized = currency_catalog.validate_code(self.value)
        object.__setattr__(self, "value", normalized)
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

    @property
    def currency(self):
        """Get the currency metadata for this code."""

        return currency_catalog.get(self.value)

    @property
    def decimal_places(self) -> int:
        """Get the number of decimal places for this code."""

        return currency_catalog.decimal_places(self.value)

    @property
    def symbol(self) -> str:
        """Get the symbol for this code."""

        return currency_catalog.symbol(self.value)

    @property
    def numeric_code(self) -> str:
        """Get the numeric code for this code."""

        return currency_catalog.numeric_code(self.value)

    @property
    def name(self) -> str:
        """Get the name for this code."""

        return currency_catalog.name(self.value)

    def validate(self):
        """
        Validation already performed during normalization.
        """

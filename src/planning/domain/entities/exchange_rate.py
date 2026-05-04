from dataclasses import dataclass
from decimal import Decimal

from src.core.domain.entities import AbstractEntity
from src.finance.domain.value_objects import CurrencyCode
from src.planning.domain.exceptions import InvalidExchangeRateError


@dataclass(kw_only=True, eq=False, repr=False)
class ExchangeRate(AbstractEntity):
    """
    Entity representing a currency exchange rate.
    """

    from_currency: CurrencyCode
    to_currency: CurrencyCode
    rate: Decimal

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """
        Validate exchange rate invariants.
        """

        if self.from_currency == self.to_currency:
            raise InvalidExchangeRateError(
                "Exchange rate currencies must be different."
            )

        if self.rate <= Decimal("0"):
            raise InvalidExchangeRateError("Exchange rate must be greater than zero.")

        if self.rate.is_nan():
            raise InvalidExchangeRateError("Exchange rate cannot be NaN.")

        if self.rate.is_infinite():
            raise InvalidExchangeRateError("Exchange rate cannot be infinite.")

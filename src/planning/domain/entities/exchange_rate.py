from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from src.core.domain.entities import AbstractEntity
from src.finance.domain.value_objects import CurrencyCode
from src.planning.domain.exceptions import InvalidExchangeRateError


@dataclass(kw_only=True, eq=False, repr=False)
class ExchangeRate(AbstractEntity):
    """
    Entity representing a currency exchange rate.
    """

    scenario_id: UUID
    from_currency: CurrencyCode
    to_currency: CurrencyCode
    rate: Decimal
    effective_date: date

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """
        Validate exchange rate invariants.
        """

        if self.from_currency == self.to_currency:
            self.notification.add_error("Exchange rate currencies must be different.")

        if self.rate <= Decimal("0"):
            self.notification.add_error("Exchange rate must be greater than zero.")

        if self.rate.is_nan():
            self.notification.add_error("Exchange rate cannot be NaN.")

        if self.rate.is_infinite():
            self.notification.add_error("Exchange rate cannot be infinite.")

        if self.notification.has_errors:
            raise InvalidExchangeRateError(self.notification.messages)

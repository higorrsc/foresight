from dataclasses import dataclass
from decimal import Decimal
from typing import SupportsInt

from src.core.domain.value_object import AbstractValueObject
from src.finance.domain.exceptions import (
    CurrencyMismatchError,
    InvalidMoneyOperationError,
)

from .currency_code import CurrencyCode


@dataclass(frozen=True, kw_only=True)
class Money(AbstractValueObject):
    """
    Monetary value object.

    Invariants:
        - amount must be Decimal
        - amount must be finite
        - precision must respect currency
    """

    amount: Decimal
    currency: CurrencyCode

    def validate(self) -> None:
        """Validate the Money object."""

        if not isinstance(self.amount, Decimal):
            raise InvalidMoneyOperationError("Money amount must be Decimal.")

        if not self.amount.is_finite():
            raise InvalidMoneyOperationError("Money amount must be finite.")

        allowed_decimals = self.currency.decimal_places

        exponent = abs(self.amount.as_tuple().exponent)  # type: ignore

        if exponent > allowed_decimals:
            raise InvalidMoneyOperationError(
                f"Currency '{self.currency}' supports "
                f"at most {allowed_decimals} decimal places."
            )

    def __add__(self, other: "Money") -> "Money":
        """Add two Money objects."""

        self._ensure_same_currency(other)

        amount = self.amount + other.amount

        return Money(
            amount=self._quantize(amount),
            currency=self.currency,
        )

    def __sub__(self, other: "Money") -> "Money":
        """Subtract two Money objects."""

        self._ensure_same_currency(other)

        amount = self.amount - other.amount

        return Money(
            amount=self._quantize(amount),
            currency=self.currency,
        )

    def __mul__(
        self,
        multiplier: Decimal | int | SupportsInt,
    ) -> "Money":
        """Multiply two Money objects."""

        decimal_multiplier = self._to_decimal(multiplier)
        amount = self.amount * decimal_multiplier

        return Money(
            amount=self._quantize(amount),
            currency=self.currency,
        )

    def __truediv__(
        self,
        divisor: Decimal | int | SupportsInt,
    ) -> "Money":
        """Divide two Money objects."""

        decimal_divisor = self._to_decimal(divisor)

        if decimal_divisor == Decimal("0"):
            raise InvalidMoneyOperationError("Division by zero is not allowed.")

        amount = self.amount / decimal_divisor

        return Money(
            amount=self._quantize(amount),
            currency=self.currency,
        )

    def __neg__(self) -> "Money":
        """Negate a Money object."""

        return Money(
            amount=-self.amount,
            currency=self.currency,
        )

    def __abs__(self) -> "Money":
        """Get the absolute value of a Money object."""

        return Money(
            amount=abs(self.amount),
            currency=self.currency,
        )

    def __lt__(self, other: "Money") -> bool:
        """Compare two Money objects."""

        self._ensure_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        """Compare two Money objects."""

        self._ensure_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: "Money") -> bool:
        """Compare two Money objects."""

        self._ensure_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        """Compare two Money objects."""

        self._ensure_same_currency(other)
        return self.amount >= other.amount

    @property
    def is_zero(self) -> bool:
        """Check if a Money object is zero."""

        return self.amount == Decimal("0")

    def _ensure_same_currency(self, other: "Money") -> None:
        """Ensure that two Money objects have the same currency."""

        if not isinstance(other, Money):
            raise InvalidMoneyOperationError(
                "Operation allowed only between Money objects."
            )

        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Currency mismatch: {self.currency} != {other.currency}"
            )

    def _quantize(self, amount: Decimal) -> Decimal:
        """Ensure decimal places"""

        decimal_places = self.currency.decimal_places

        quantizer = Decimal("1" if decimal_places == 0 else f"1.{'0' * decimal_places}")

        return amount.quantize(quantizer)

    @staticmethod
    def _to_decimal(
        value: Decimal | int | SupportsInt,
    ) -> Decimal:
        """Convert a value to a Decimal object."""

        if isinstance(value, float):
            raise InvalidMoneyOperationError("Float values are not supported.")

        return Decimal(value)  # type: ignore

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

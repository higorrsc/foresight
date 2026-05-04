from dataclasses import dataclass
from decimal import Decimal
from typing import SupportsInt

from src.core.domain.exceptions import EntityValidationError
from src.core.domain.value_object import AbstractValueObject
from src.finance.domain.constants import CURRENCY_DECIMAL_PLACES
from src.finance.domain.exceptions import (
    CurrencyMismatchError,
    InvalidMoneyOperationError,
)
from src.finance.domain.value_objects import CurrencyCode


@dataclass(frozen=True, kw_only=True, slots=True)
class Money(AbstractValueObject):
    """
    Value object representing a monetary amount in a specific currency.

    Invariants:
        - amount must be a Decimal
        - amount cannot be NaN
        - amount cannot be infinite
        - amount precision must respect the currency decimal places
    """

    amount: Decimal
    currency: CurrencyCode

    def __post_init__(self) -> None:
        """
        Normalize and validate the monetary amount.
        """

        normalized_amount = self._normalize_amount(self.amount)
        object.__setattr__(self, "amount", normalized_amount)
        super().__post_init__()

    def validate(self) -> None:
        """
        Validate monetary invariants.

        Raises:
            EntityValidationError:
                If the monetary value is invalid.
        """

        if not isinstance(self.amount, Decimal):
            raise EntityValidationError("Money amount must be a Decimal.")

        if self.amount.is_nan():
            raise EntityValidationError("Money amount cannot be NaN.")

        if self.amount.is_infinite():
            raise EntityValidationError("Money amount cannot be infinite.")

        allowed_decimals = CURRENCY_DECIMAL_PLACES[str(self.currency)]

        exponent = abs(self.amount.as_tuple().exponent)  # type: ignore

        if exponent > allowed_decimals:
            raise EntityValidationError(
                f"Currency '{self.currency}' supports at most "
                f"{allowed_decimals} decimal places."
            )

    def __add__(self, other: "Money") -> "Money":
        """
        Add two Money objects.

        Raises:
            InvalidMoneyOperationError:
                If the other object is not Money.

            CurrencyMismatchError:
                If currencies are different.
        """

        self._ensure_same_currency(other)

        return Money(
            amount=self.amount + other.amount,
            currency=self.currency,
        )

    def __sub__(self, other: "Money") -> "Money":
        """
        Subtract two Money objects.

        Raises:
            InvalidMoneyOperationError:
                If the other object is not Money.

            CurrencyMismatchError:
                If currencies are different.
        """

        self._ensure_same_currency(other)

        return Money(
            amount=self.amount - other.amount,
            currency=self.currency,
        )

    def __mul__(
        self,
        multiplier: Decimal | int | SupportsInt,
    ) -> "Money":
        """
        Multiply Money by a numeric value.

        Float values are intentionally not supported to avoid
        floating-point precision issues.

        Raises:
            InvalidMoneyOperationError:
                If multiplier is a float.
        """

        if isinstance(multiplier, float):
            raise InvalidMoneyOperationError(
                "Float values are not supported in Money operations."
            )

        return Money(
            amount=self.amount * Decimal(multiplier),  # type: ignore
            currency=self.currency,
        )

    def __truediv__(
        self,
        divisor: Decimal | int | SupportsInt,
    ) -> "Money":
        """
        Divide Money by a numeric value.

        Raises:
            InvalidMoneyOperationError:
                If divisor is zero or float.
        """

        if isinstance(divisor, float):
            raise InvalidMoneyOperationError(
                "Float values are not supported in Money operations."
            )

        decimal_divisor = Decimal(divisor)  # type: ignore

        if decimal_divisor == Decimal("0"):
            raise InvalidMoneyOperationError("Division by zero is not allowed.")

        return Money(
            amount=self.amount / decimal_divisor,
            currency=self.currency,
        )

    def __neg__(self) -> "Money":
        """
        Negate Money amount.
        """

        return Money(
            amount=-self.amount,
            currency=self.currency,
        )

    def __abs__(self) -> "Money":
        """
        Return absolute Money value.
        """

        return Money(
            amount=abs(self.amount),
            currency=self.currency,
        )

    def __lt__(self, other: "Money") -> bool:
        """
        Compare if Money is less than another Money.
        """

        self._ensure_same_currency(other)

        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        """
        Compare if Money is less than or equal to another Money.
        """

        self._ensure_same_currency(other)

        return self.amount <= other.amount

    def __gt__(self, other: "Money") -> bool:
        """
        Compare if Money is greater than another Money.
        """

        self._ensure_same_currency(other)

        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        """
        Compare if Money is greater than or equal to another Money.
        """

        self._ensure_same_currency(other)

        return self.amount >= other.amount

    @property
    def is_zero(self) -> bool:
        """
        Indicates whether the monetary amount is zero.
        """

        return self.amount == Decimal("0")

    def _ensure_same_currency(self, other: "Money") -> None:
        """
        Ensure Money operations use the same currency.

        Raises:
            InvalidMoneyOperationError:
                If the other object is not Money.

            CurrencyMismatchError:
                If currencies are different.
        """

        if not isinstance(other, Money):
            raise InvalidMoneyOperationError(
                "Operation allowed only between Money objects."
            )

        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Currency mismatch: {self.currency} != {other.currency}"
            )

    def _normalize_amount(self, amount: Decimal) -> Decimal:
        """
        Normalize amount precision according to currency.

        Returns:
            Decimal:
                Quantized monetary amount.
        """

        decimal_places = CURRENCY_DECIMAL_PLACES[str(self.currency)]

        quantizer = Decimal("1" if decimal_places == 0 else f"1.{'0' * decimal_places}")

        return amount.quantize(quantizer)

    def __str__(self) -> str:
        """
        String representation of Money.
        """

        return f"{self.amount} {self.currency}"

    def __repr__(self) -> str:
        """
        Debug representation of Money.
        """

        return f"Money(amount={self.amount}, currency='{self.currency}')"

from decimal import Decimal

import pytest

from src.core.domain import EntityValidationError
from src.finance.domain.exceptions import (
    CurrencyMismatchError,
    InvalidMoneyOperationError,
)
from src.finance.domain.value_objects import CurrencyCode, Money


class TestMoney:
    """
    Test suite for the Money value object.
    """

    def test_money_initialization_success(self, brl_currency):
        """
        Test successful initialization and normalization of Money.
        """
        money = Money(amount=Decimal("100.555"), currency=brl_currency)
        # BRL has 2 decimal places, so it should be rounded/quantized
        assert money.amount == Decimal("100.56")
        assert money.currency == brl_currency
        assert str(money) == "100.56 BRL"
        assert repr(money) == "Money(amount=100.56, currency='BRL')"

    def test_money_initialization_zero_decimals(self):
        """
        Test initialization for currency with zero decimal places (JPY).
        """
        jpy = CurrencyCode(value="JPY")
        money = Money(amount=Decimal("100.7"), currency=jpy)
        assert money.amount == Decimal("101")

    def test_money_validation_failure(self, brl_currency):
        """
        Test validation failures for Money.
        """
        with pytest.raises(
            EntityValidationError,
            match="Money amount must be a Decimal.",
        ):
            Money(amount="100", currency=brl_currency)  # type: ignore

        with pytest.raises(
            EntityValidationError,
            match="Money amount cannot be NaN.",
        ):
            Money(amount=Decimal("NaN"), currency=brl_currency)

        with pytest.raises(
            EntityValidationError,
            match="Money amount cannot be infinite.",
        ):
            Money(amount=Decimal("Infinity"), currency=brl_currency)

    def test_money_add_success(self, money_brl_100, brl_currency):
        """
        Test addition of two Money objects with the same currency.
        """
        other = Money(amount=Decimal("50.00"), currency=brl_currency)
        result = money_brl_100 + other
        assert result.amount == Decimal("150.00")
        assert result.currency == brl_currency

    def test_money_add_mismatch_currency(self, money_brl_100, money_usd_100):
        """
        Test addition failure due to currency mismatch.
        """
        with pytest.raises(CurrencyMismatchError):
            _ = money_brl_100 + money_usd_100

    def test_money_sub_success(self, money_brl_100, brl_currency):
        """
        Test subtraction of two Money objects with the same currency.
        """
        other = Money(amount=Decimal("40.00"), currency=brl_currency)
        result = money_brl_100 - other
        assert result.amount == Decimal("60.00")

    def test_money_mul_success(self, money_brl_100):
        """
        Test multiplication by numeric values.
        """
        result = money_brl_100 * 2
        assert result.amount == Decimal("200.00")

        result = money_brl_100 * Decimal("1.5")
        assert result.amount == Decimal("150.00")

    def test_money_mul_float_failure(self, money_brl_100):
        """
        Test multiplication failure when using float.
        """
        with pytest.raises(
            InvalidMoneyOperationError, match="Float values are not supported"
        ):
            _ = money_brl_100 * 1.5

    def test_money_div_success(self, money_brl_100):
        """
        Test division by numeric values.
        """
        result = money_brl_100 / 2
        assert result.amount == Decimal("50.00")

    def test_money_div_zero_failure(self, money_brl_100):
        """
        Test division by zero.
        """
        with pytest.raises(
            InvalidMoneyOperationError, match="Division by zero is not allowed."
        ):
            _ = money_brl_100 / 0

    def test_money_negation_and_abs(self, money_brl_100):
        """
        Test negation and absolute value.
        """
        neg_money = -money_brl_100
        assert neg_money.amount == Decimal("-100.00")

        abs_money = abs(neg_money)
        assert abs_money.amount == Decimal("100.00")

    def test_money_comparisons(self, money_brl_100, brl_currency):
        """
        Test comparison operators between Money objects.
        """
        more = Money(amount=Decimal("150.00"), currency=brl_currency)
        less = Money(amount=Decimal("50.00"), currency=brl_currency)
        equal = Money(amount=Decimal("100.00"), currency=brl_currency)

        assert money_brl_100 < more
        assert money_brl_100 <= more
        assert money_brl_100 > less
        assert money_brl_100 >= less
        assert money_brl_100 == equal
        assert money_brl_100 <= equal
        assert money_brl_100 >= equal

    def test_money_is_zero(self, brl_currency):
        """
        Test is_zero property.
        """
        zero = Money(amount=Decimal("0.00"), currency=brl_currency)
        not_zero = Money(amount=Decimal("0.01"), currency=brl_currency)

        assert zero.is_zero is True
        assert not_zero.is_zero is False

    def test_money_ensure_same_currency_error(self, money_brl_100):
        """
        Test that operations only allow Money objects.
        """
        with pytest.raises(
            InvalidMoneyOperationError,
            match="Operation allowed only between Money objects.",
        ):
            _ = money_brl_100 + "100"  # type: ignore

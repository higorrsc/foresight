from dataclasses import dataclass
from decimal import Decimal

from core.domain._shared.value_object import AbstractValueObject


@dataclass(kw_only=True)
class DummyValueObjectForMoneyType(AbstractValueObject):
    """
    A dummy value object for money type.
    """

    amount: Decimal
    currency: str

    def _validate(self):
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


class TestAbstractValueObject:
    """
    Test cases for the AbstractValueObject class.
    """

    def test_concrete_value_object_instantiation(self):
        """
        Test that instantiating a concrete subclass of AbstractValueObject works.
        """

        my_money = DummyValueObjectForMoneyType(amount=Decimal("10.00"), currency="USD")
        assert my_money.amount == Decimal("10.00")
        assert my_money.currency == "USD"

    def test_validate_empty_amount(self):
        """
        Test the validation of an empty amount.
        """

        try:
            DummyValueObjectForMoneyType(
                amount=None,  # type: ignore
                currency="USD",
            )  # ❌ amount is None
        except ValueError as e:
            assert str(e) == "Amount cannot be empty"
        else:
            assert False, "ValueError was not raised"

    def test_validate_invalid_amount(self):
        """
        Test the validation of an invalid amount.
        """

        try:
            DummyValueObjectForMoneyType(
                amount="10.00",  # type: ignore
                currency="USD",
            )  # ❌ amount is not Decimal
        except ValueError as e:
            assert str(e) == "Amount must be a decimal"
        else:
            assert False, "ValueError was not raised"

    def test_validate_currency_characters(self):
        """
        Test the validation of currency with invalid length.
        """

        try:
            DummyValueObjectForMoneyType(
                amount=Decimal("10.00"),
                currency="US",  # ❌ currency length is not 3
            )
        except ValueError as e:
            assert str(e) == "Currency must be exactly 3 characters long"
        else:
            assert False, "ValueError was not raised"

    def test_validate_empty_currency(self):
        """
        Test the validation of an empty currency.
        """

        try:
            DummyValueObjectForMoneyType(
                amount=Decimal("10.00"),
                currency="",  # ❌ currency is empty
            )
        except ValueError as e:
            assert str(e) == "Currency cannot be empty"
        else:
            assert False, "ValueError was not raised"

    def test_validate_invalid_currency(self):
        """
        Test the validation of an invalid currency.
        """

        try:
            DummyValueObjectForMoneyType(
                amount=Decimal("10.00"),
                currency=123,  # type: ignore ❌ currency is not a string
            )
        except ValueError as e:
            assert str(e) == "Currency must be a string"
        else:
            assert False, "ValueError was not raised"

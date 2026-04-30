from decimal import Decimal

from tests.fakes import DummyValueObjectForMoneyType


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
            raise AssertionError("ValueError was not raised")

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
            raise AssertionError("ValueError was not raised")

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
            raise AssertionError("ValueError was not raised")

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
            raise AssertionError("ValueError was not raised")

    def test_validate_invalid_currency(self):
        """
        Test the validation of an invalid currency.
        """

        try:
            DummyValueObjectForMoneyType(
                amount=Decimal("10.00"),
                currency=123,  # type: ignore
            )
        except ValueError as e:
            assert str(e) == "Currency must be a string"
        else:
            raise AssertionError("ValueError was not raised")

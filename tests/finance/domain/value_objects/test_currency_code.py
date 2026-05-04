import pytest

from src.core.domain import EntityValidationError
from src.finance.domain.value_objects import CurrencyCode


class TestCurrencyCode:
    """
    Test suite for the CurrencyCode value object.
    """

    def test_currency_code_initialization_success(self):
        """
        Test successful initialization of CurrencyCode with valid values.
        """
        code = CurrencyCode(value="brl")
        assert code.value == "BRL"
        assert str(code) == "BRL"
        assert repr(code) == "<CurrencyCode value=BRL>"

    @pytest.mark.parametrize(
        "invalid_value, expected_error",
        [
            ("BR", "Currency code must be 3 characters long"),
            ("BRL1", "Currency code must be 3 characters long"),
            ("B1L", "Currency code must contain only letters"),
            ("ZZZ", "Invalid ISO 4217 currency code: ZZZ"),
        ],
    )
    def test_currency_code_validation_failure(self, invalid_value, expected_error):
        """
        Test initialization failure with invalid currency codes.
        """
        with pytest.raises(EntityValidationError, match=expected_error):
            CurrencyCode(value=invalid_value)

    def test_currency_code_equality(self):
        """
        Test equality comparison between CurrencyCode objects.
        """
        code1 = CurrencyCode(value="BRL")
        code2 = CurrencyCode(value="brl")
        code3 = CurrencyCode(value="USD")

        assert code1 == code2
        assert code1 != code3
        assert hash(code1) == hash(code2)

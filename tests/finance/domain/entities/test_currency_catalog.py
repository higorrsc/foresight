import pytest

from src.finance.domain.entities.currency import (
    Currency,
    currency_catalog,
    load_currency_catalog,
)
from src.finance.domain.exceptions import InvalidCurrencyCodeError


class TestCurrencyCatalog:
    """
    Test suite for CurrencyCatalog.
    """

    def test_currency_exists(self):
        """
        Test currency existence lookup.
        """

        assert currency_catalog.exists("BRL") is True
        assert currency_catalog.exists("USD") is True
        assert currency_catalog.exists("ZZZ") is False

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("brl", "BRL"),
            (" BRL ", "BRL"),
            ("usd", "USD"),
            (" jpy ", "JPY"),
        ],
    )
    def test_validate_code_success(
        self,
        value,
        expected,
    ):
        """
        Test successful currency normalization and validation.
        """

        result = currency_catalog.validate_code(value)

        assert result == expected

    @pytest.mark.parametrize(
        "value, expected_error",
        [
            (
                123,
                "Currency code must be a string",
            ),
            (
                "BR",
                "Currency code must contain 3 characters",
            ),
            (
                "BRL1",
                "Currency code must contain 3 characters",
            ),
            (
                "B1L",
                "Currency code must contain only letters",
            ),
            (
                "ZZZ",
                "Unsupported ISO 4217 currency code: ZZZ",
            ),
        ],
    )
    def test_validate_code_failure(
        self,
        value,
        expected_error,
    ):
        """
        Test invalid currency codes.
        """

        with pytest.raises(
            InvalidCurrencyCodeError,
            match=expected_error,
        ):
            currency_catalog.validate_code(value)

    def test_get_currency_success(self):
        """
        Test retrieving a currency.
        """

        currency = currency_catalog.get("BRL")

        assert isinstance(currency, Currency)
        assert currency.code == "BRL"
        assert currency.symbol == "R$"
        assert currency.decimal_places == 2

    def test_get_currency_not_found(self):
        """
        Test retrieval failure for unknown currency.
        """

        with pytest.raises(
            InvalidCurrencyCodeError,
            match="Unsupported ISO 4217 currency code: ZZZ",
        ):
            currency_catalog.get("ZZZ")

    def test_decimal_places(self):
        """
        Test decimal places lookup.
        """

        assert currency_catalog.decimal_places("BRL") == 2
        assert currency_catalog.decimal_places("USD") == 2
        assert currency_catalog.decimal_places("JPY") == 0

    def test_symbol(self):
        """
        Test currency symbol lookup.
        """

        assert currency_catalog.symbol("BRL") == "R$"
        assert currency_catalog.symbol("USD") == "$"
        assert currency_catalog.symbol("JPY") == "¥"

    def test_numeric_code(self):
        """
        Test numeric code lookup.
        """

        assert currency_catalog.numeric_code("BRL") == "986"
        assert currency_catalog.numeric_code("USD") == "840"
        assert currency_catalog.numeric_code("JPY") == "392"

    def test_name(self):
        """
        Test currency name lookup.
        """

        assert currency_catalog.name("BRL") == "Brazilian Real"
        assert currency_catalog.name("USD") == "United States Dollar"
        assert currency_catalog.name("JPY") == "Japanese Yen"

    def test_codes_property(self):
        """
        Test available currency codes.
        """

        codes = currency_catalog.codes

        assert isinstance(codes, frozenset)

        assert "BRL" in codes
        assert "USD" in codes
        assert "JPY" in codes

    def test_all_property(self):
        """
        Test retrieval of all currencies.
        """

        currencies = currency_catalog.all

        assert isinstance(currencies, tuple)

        assert len(currencies) > 0

        assert all(isinstance(currency, Currency) for currency in currencies)

    def test_catalog_is_cached(self):
        """
        Test singleton cache behavior.
        """

        assert load_currency_catalog() is load_currency_catalog()

from functools import cache
from pathlib import Path
from types import MappingProxyType
from typing import Final

import yaml

from src.finance.domain.exceptions import (
    CurrencyNotFoundError,
    InvalidCurrencyCodeError,
)

from .models import Currency

BASE_DIR: Final = Path(__file__).resolve().parent
CURRENCIES_FILE: Final = BASE_DIR / "currencies.yaml"


class CurrencyCatalog:
    """
    Read-only currency catalog.
    """

    def __init__(self, currencies: dict[str, Currency]):
        """Create a new currency catalog."""
        self._currencies = MappingProxyType(currencies)

    def exists(self, code: str) -> bool:
        """Check if a currency exists."""

        return code.upper() in self._currencies

    def validate_code(self, code: str) -> str:
        """Validate a currency code and normalize it."""

        if not isinstance(code, str):
            raise InvalidCurrencyCodeError("Currency code must be a string")

        normalized = code.strip().upper()

        if len(normalized) != 3:
            raise InvalidCurrencyCodeError("Currency code must contain 3 characters")

        if not normalized.isalpha():
            raise InvalidCurrencyCodeError("Currency code must contain only letters")

        if normalized not in self._currencies:
            raise InvalidCurrencyCodeError(
                f"Unsupported ISO 4217 currency code: {normalized}"
            )

        return normalized

    def get(self, code: str) -> Currency:
        """Get a currency by code."""

        normalized = self.validate_code(code)

        try:
            return self._currencies[normalized]
        except KeyError as exc:
            raise CurrencyNotFoundError(f"Currency not found: {normalized}") from exc

    def decimal_places(self, code: str) -> int:
        """Get the number of decimal places for a currency."""

        return self.get(code).decimal_places

    def symbol(self, code: str) -> str:
        """Get the symbol for a currency."""

        return self.get(code).symbol

    def numeric_code(self, code: str) -> str:
        """Get the numeric code for a currency."""

        return self.get(code).numeric_code

    def name(self, code: str) -> str:
        """Get the name for a currency."""

        return self.get(code).name

    @property
    def codes(self) -> frozenset[str]:
        """Get the codes for all currencies."""

        return frozenset(self._currencies.keys())

    @property
    def all(self) -> tuple[Currency, ...]:
        """Get all currencies."""

        return tuple(self._currencies.values())


@cache
def load_currency_catalog() -> CurrencyCatalog:
    """Load the currency catalog from the YAML file."""

    with CURRENCIES_FILE.open(encoding="utf-8") as file:
        raw_data = yaml.safe_load(file)

    currencies = {
        code.upper(): Currency(
            code=code.upper(),
            **metadata,
        )
        for code, metadata in raw_data.items()
    }

    return CurrencyCatalog(currencies)


currency_catalog: Final = load_currency_catalog()

from dataclasses import dataclass, field
from enum import StrEnum

from src.core.domain.entities import DescribedEntity
from src.core.domain.mixins import SoftDeletableMixin, UserAuditMixin

from .exchange_rate import ExchangeRate


class ScenarioType(StrEnum):
    """
    Enum representing the types of financial scenarios.
    """

    BUDGET = "BUDGET"
    ACTUAL = "ACTUAL"
    FORECAST = "FORECAST"


@dataclass(kw_only=True, eq=False, repr=False)
class Scenario(DescribedEntity, SoftDeletableMixin, UserAuditMixin):
    """
    Entity representing a financial scenario within the system.
    """

    scenario_type: ScenarioType
    is_locked: bool = False
    assumptions: str | None
    exchange_rates: list[ExchangeRate] = field(default_factory=list)

    def add_exchange_rate(self, rate: "ExchangeRate") -> None:
        """
        Add new exchange rate to scenario.
        """

        for existing in self.exchange_rates:
            if (
                existing.from_currency == rate.from_currency
                and existing.to_currency == rate.to_currency
                and existing.effective_date == rate.effective_date
            ):
                raise ValueError(
                    f"Já existe uma taxa de {rate.from_currency} "
                    f"para {rate.to_currency} na data {rate.effective_date}."
                )

        self.exchange_rates.append(rate)

    def lock(self) -> None:
        """
        Locks the financial scenario.
        """

        self.is_locked = True

    def unlock(self) -> None:
        """
        Unlocks the financial scenario.
        """

        self.is_locked = False

    def _str_fields(self) -> str:
        """
        Returns a string representation of the fields of the Scenario entity.
        """

        return f"id={self.id}, description='{self.description}'"

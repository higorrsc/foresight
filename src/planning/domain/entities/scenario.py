from dataclasses import dataclass
from enum import StrEnum

from src.core.domain.entities import DescribedEntity
from src.core.domain.mixins import SoftDeletableMixin, UserAuditMixin


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

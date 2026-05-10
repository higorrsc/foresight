from decimal import Decimal

from src.core.infrastructure.mappers import AbstractMapper
from src.finance.domain.value_objects import CurrencyCode
from src.planning.domain.entities import ExchangeRate
from src.planning.infrastructure.models import ExchangeRateModel


class ExchangeRateMapper(AbstractMapper[ExchangeRate, ExchangeRateModel]):
    """
    Mapper class to convert between ExchangeRate entity and ExchangeRateModel.
    """

    def to_model(self, entity: ExchangeRate) -> ExchangeRateModel:
        """
        Converts an ExchangeRate entity to an ExchangeRateModel instance.
        """

        return ExchangeRateModel(
            id=entity.id,
            scenario_id=entity.scenario_id,
            from_currency=str(entity.from_currency),
            to_currency=str(entity.to_currency),
            rate=entity.rate,
        )

    def to_entity(self, model: ExchangeRateModel) -> ExchangeRate:
        """
        Converts an ExchangeRateModel instance to an ExchangeRate entity.
        """

        return ExchangeRate(
            id=model.id,  # type: ignore
            scenario_id=model.scenario_id,  # type: ignore
            from_currency=CurrencyCode(value=model.from_currency),  # type: ignore
            to_currency=CurrencyCode(value=model.to_currency),  # type: ignore
            rate=Decimal(str(model.rate)),  # type: ignore
        )

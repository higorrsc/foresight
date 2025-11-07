from decimal import Decimal

from src.tenant_management.domain.entities import Plan
from src.tenant_management.infrastructure.models import PlanModel


class PlanMapper:
    """
    Mapper class to convert between Plan entity and PlanModel.
    """

    @staticmethod
    def to_model(entity: Plan) -> PlanModel:
        """
        Converts a Plan entity to a PlanModel instance.
        """

        return PlanModel(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )

    @staticmethod
    def to_entity(model: PlanModel) -> Plan:
        """
        Converts a PlanModel instance to a Plan entity.
        """

        return Plan(
            id=model.id,  # type: ignore
            name=model.name,  # type: ignore
            price=Decimal(model.price),  # type: ignore
            created_by=model.created_by,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_by=model.updated_by,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

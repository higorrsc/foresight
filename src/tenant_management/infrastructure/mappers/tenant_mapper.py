from src.tenant_management.domain.entities import Tenant
from src.tenant_management.infrastructure.models import TenantModel


class TenantMapper:
    """
    Mapper class to convert between Tenant entity and TenantModel.
    """

    @staticmethod
    def to_model(entity: Tenant) -> "TenantModel":
        """
        Converts a Tenant entity to a TenantModel instance.
        """

        return TenantModel(
            id=entity.id,
            name=entity.name,
            status=entity.status,
            plan_id=entity.plan_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_entity(model: "TenantModel") -> Tenant:
        """
        Converts a TenantModel instance to a Tenant entity.
        """

        return Tenant(
            id=model.id,  # type: ignore
            name=model.name,  # type: ignore
            status=model.status,  # type: ignore
            plan_id=model.plan_id,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

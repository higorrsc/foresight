from src.core.infrastructure.mappers import AbstractMapper, BaseMapper
from src.tenant_management.domain.entities import Tenant
from src.tenant_management.infrastructure.models import TenantModel


class TenantMapper(AbstractMapper[Tenant, TenantModel]):
    """
    Mapper class to convert between Tenant entity and TenantModel.
    """

    @staticmethod
    def to_model(entity: Tenant) -> TenantModel:
        """
        Converts a Tenant entity to a TenantModel instance.
        """

        model = TenantModel(
            id=entity.id,
            name=entity.name,
            status=entity.status,
            plan_id=entity.plan_id,
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return model

    @staticmethod
    def to_entity(model: TenantModel) -> Tenant:
        """
        Converts a TenantModel instance to a Tenant entity.
        """

        entity = Tenant(
            id=model.id,  # type: ignore
            name=model.name,  # type: ignore
            status=model.status,  # type: ignore
            plan_id=model.plan_id,  # type: ignore
        )

        BaseMapper.map_auditing_fields_to_entity(model, entity)
        return entity

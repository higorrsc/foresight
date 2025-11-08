from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.infrastructure.mappers._shared import BaseMapper
from src.shared_kernel.infrastructure.models import OrganizationalUnitModel


class OrganizationalUnitMapper:
    """
    Mapper class to convert between OrganizationalUnit entity and OrganizationalUnitModel
    """

    @staticmethod
    def to_model(entity: OrganizationalUnit) -> OrganizationalUnitModel:
        """
        Convert an OrganizationalUnit entity to an OrganizationalModel instance
        """

        model = OrganizationalUnitModel(
            id=entity.id,
            tenant_id=entity.tenant_id,
            code=entity.code,
            description=entity.description,
            parent_id=entity.parent_id,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return model

    @staticmethod
    def to_entity(model: OrganizationalUnitModel) -> OrganizationalUnit:
        """
        Converts an OrganizationalUnitModel instance to an OrganizationalUnit
        """

        entity = OrganizationalUnit(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            code=model.code,  # type: ignore
            description=model.description,  # type: ignore
            parent_id=model.parent_id,  # type: ignore
            is_active=model.is_active,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return entity

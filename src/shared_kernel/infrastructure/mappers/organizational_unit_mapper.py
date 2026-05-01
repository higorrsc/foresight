from src.core.infrastructure.mappers import AbstractMapper, BaseMapper
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.infrastructure.models import OrganizationalUnitModel


class OrganizationalUnitMapper(
    AbstractMapper[OrganizationalUnit, OrganizationalUnitModel]
):
    """
    Mapper class to convert between OrganizationalUnit entity
    and OrganizationalUnitModel
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
        )

        BaseMapper.map_auditing_fields_to_entity(model, entity)
        return entity

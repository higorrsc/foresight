from src.core.infrastructure.mappers import AbstractMapper, BaseMapper
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.infrastructure.models import AreaModel


class AreaMapper(AbstractMapper[Area, AreaModel]):
    """
    Mapper class to convert between Area entity and AreaModel.
    """

    @staticmethod
    def to_model(entity: Area) -> AreaModel:
        """
        Converts an Area entity to an AreaModel instance.
        """

        model = AreaModel(
            id=entity.id,
            tenant_id=entity.tenant_id,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return model

    @staticmethod
    def to_entity(model: AreaModel) -> Area:
        """
        Converts an AreaModel instance to an Area entity.
        """

        entity = Area(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            description=model.description,  # type: ignore
            is_active=model.is_active,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

        BaseMapper.map_auditing_fields_to_entity(model, entity)
        return entity

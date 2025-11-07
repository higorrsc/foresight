from src.shared_kernel.domain.entities import Area
from src.shared_kernel.infrastructure.models import AreaModel


class AreaMapper:
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
            created_by=entity.created_by,
            created_at=entity.created_at,
            updated_by=entity.updated_by,
            updated_at=entity.updated_at,
        )

        if hasattr(entity, "deleted_at"):
            model.deleted_at = entity.deleted_at  # type: ignore

        return model

    @staticmethod
    def to_entity(model: AreaModel) -> Area:
        """
        Converts an AreaModel instance to an Area entity.
        """

        area = Area(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            description=model.description,  # type: ignore
            is_active=model.is_active,  # type: ignore
            created_by=model.created_by,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_by=model.updated_by,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

        if hasattr(model, "deleted_at") and hasattr(area, "deleted_at"):
            setattr(area, "deleted_at", model.deleted_at)

        return area

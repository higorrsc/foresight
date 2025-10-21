from src.core.domain.entities import Area
from src.core.infrastructure.models import AreaModel


class AreaMapper:
    """
    Mapper class to convert between Area entity and AreaModel.
    """

    @staticmethod
    def to_model(entity: Area) -> "AreaModel":
        """
        Converts an Area entity to an AreaModel instance.
        """

        return AreaModel(
            id=entity.id,
            description=entity.description,
            is_active=entity.is_active,
            deleted_at=getattr(entity, "deleted_at", None),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_entity(model: "AreaModel") -> Area:
        """
        Converts an AreaModel instance to an Area entity.
        """

        area = Area(
            id=model.id,  # type: ignore
            description=model.description,  # type: ignore
            is_active=model.is_active,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

        if hasattr(model, "deleted_at") and hasattr(area, "deleted_at"):
            setattr(area, "deleted_at", model.deleted_at)

        return area

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
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_entity(model: "AreaModel") -> Area:
        """
        Converts an AreaModel instance to an Area entity.
        """

        return Area(
            id=model.id,  # type: ignore
            description=model.description,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

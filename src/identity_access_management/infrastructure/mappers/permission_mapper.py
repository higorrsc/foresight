from src.core.infrastructure.mappers import AbstractMapper
from src.identity_access_management.domain.entities import Permission
from src.identity_access_management.infrastructure.models import PermissionModel


class PermissionMapper(AbstractMapper[Permission, PermissionModel]):
    """
    Mapper class to convert between Permission entity and PermissionModel.
    """

    @staticmethod
    def to_model(entity: Permission) -> PermissionModel:
        """
        Converts a Permission entity to a PermissionModel instance.
        """

        return PermissionModel(
            id=entity.id,
            codename=entity.codename,
            description=entity.description,
        )

    @staticmethod
    def to_entity(model: PermissionModel) -> Permission:
        """
        Converts a PermissionModel instance to a Permission entity.
        """

        return Permission(
            id=model.id,  # type: ignore
            codename=model.codename,  # type: ignore
            description=model.description,  # type: ignore
        )

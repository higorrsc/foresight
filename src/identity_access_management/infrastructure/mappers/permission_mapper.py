from src.identity_access_management.domain.entities import Permission
from src.identity_access_management.infrastructure.models import PermissionModel


class PermissionMapper:
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
            created_by=entity.created_by,
            created_at=entity.created_at,
            updated_by=entity.updated_by,
            updated_at=entity.updated_at,
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
            created_by=model.created_by,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_by=model.updated_by,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

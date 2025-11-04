from src.identity_access_management.domain.entities import Role
from src.identity_access_management.infrastructure.models import RoleModel


class RoleMapper:
    """
    Mapper class to convert between Role entity and RoleModel.
    """

    @staticmethod
    def to_model(entity: "Role") -> "RoleModel":
        """
        Converts a Role entity to a RoleModel instance.
        """

        return RoleModel(
            id=entity.id,
            tenant_id=entity.tenant_id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_entity(model: "RoleModel") -> "Role":
        """
        Converts a RoleModel instance to a Role entity.
        """
        permission_codes = (
            {permission.codename for permission in model.permissions}
            if model.permissions
            else set()
        )

        return Role(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            name=model.name,  # type: ignore
            description=model.description,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
            permissions=permission_codes,
        )

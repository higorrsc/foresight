from src.identity_access_management.domain.entities import Role
from src.identity_access_management.infrastructure.models import RoleModel
from src.shared_kernel.infrastructure.mappers._shared import BaseMapper


class RoleMapper:
    """
    Mapper class to convert between Role entity and RoleModel.
    """

    @staticmethod
    def to_model(entity: Role) -> RoleModel:
        """
        Converts a Role entity to a RoleModel instance.
        """

        model = RoleModel(
            id=entity.id,
            tenant_id=entity.tenant_id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return model

    @staticmethod
    def to_entity(model: RoleModel) -> Role:
        """
        Converts a RoleModel instance to a Role entity.
        """
        permission_codes = (
            {permission.codename for permission in model.permissions_rel}
            if model.permissions_rel
            else set()
        )

        entity = Role(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            name=model.name,  # type: ignore
            description=model.description,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
            permissions=permission_codes,  # type: ignore
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return entity

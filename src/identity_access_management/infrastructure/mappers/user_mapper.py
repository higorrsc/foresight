from src.identity_access_management.domain.entities import User
from src.identity_access_management.infrastructure.models import UserModel
from src.shared_kernel.infrastructure.mappers._shared.base_mapper import BaseMapper


class UserMapper:
    """
    Mapper class to convert between User entity and UserModel.
    """

    @staticmethod
    def to_model(entity: User) -> UserModel:
        """
        Converts a User entity to a UserModel instance.
        """

        model = UserModel(
            id=entity.id,
            tenant_id=entity.tenant_id,
            username=entity.username,
            hashed_password=entity.hashed_password,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return model

    @staticmethod
    def to_entity(model: UserModel) -> User:
        """
        Converts a UserModel instance to a User entity.
        """

        role_names = {role.name for role in model.roles} if model.roles else set()
        effective_permissions = set()

        if model.permissions:
            for permission in model.permissions:
                effective_permissions.add(permission.codename)

        if model.roles:
            for role in model.roles:
                for permission in role.permissions:
                    effective_permissions.add(permission.codename)

        entity = User(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            username=model.username,  # type: ignore
            hashed_password=model.hashed_password,  # type: ignore
            first_name=model.first_name,  # type: ignore
            last_name=model.last_name,  # type: ignore
            email=model.email if model.email else None,  # type: ignore
            is_active=model.is_active,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
            roles=role_names,  # type: ignore
            permissions=effective_permissions,  # type: ignore
        )

        BaseMapper.map_auditing_fields_to_entity(model, entity)
        return entity

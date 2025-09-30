from src.core.domain.entities import User
from src.core.infrastructure.models import UserModel


class UserMapper:
    """
    Mapper class to convert between User entity and UserModel.
    """

    @staticmethod
    def to_model(entity: User) -> "UserModel":
        """
        Converts a User entity to a UserModel instance.
        """

        return UserModel(
            id=entity.id,
            username=entity.username,
            password=entity.hashed_password,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_entity(model: "UserModel") -> User:
        """
        Converts a UserModel instance to a User entity.
        """

        role_names = {role.name for role in model.roles} if model.roles else set()
        return User(
            id=model.id,  # type: ignore
            username=model.username,  # type: ignore
            hashed_password=model.password,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
            roles=role_names,
        )

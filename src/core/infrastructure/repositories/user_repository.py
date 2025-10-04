from typing import Optional

from sqlalchemy.orm import Session

from src.core.domain.entities.user import User
from src.core.infrastructure.mappers import UserMapper
from src.core.infrastructure.models import RoleModel, UserModel
from src.core.infrastructure.repositories._shared import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User, UserModel]):
    """
    Repository for managing User entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the UserRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, UserModel, mapper=UserMapper)

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by its username.

        :param username: Username of the user.
        :return: User entity or None if not found.
        """

        model = (
            self._session.query(self._model_cls).filter_by(username=username).first()
        )
        return self._mapper.to_entity(model) if model else None

    def save(self, entity: User) -> Optional[User]:
        """
        Save User entity
        """

        model = self._mapper.to_model(entity)

        if entity.roles:
            role_models = (
                self._session.query(RoleModel)
                .filter(RoleModel.name.in_(entity.roles))
                .all()
            )
            model.roles = role_models

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)

        return self._mapper.to_entity(model)

    def update(self, entity: User) -> Optional[User]:
        """
        Update User entity
        """

        model = self._session.query(self._model_cls).get(entity.id)
        if not model:
            return None

        model.username = entity.username
        model.hashed_password = entity.hashed_password
        model.first_name = entity.first_name
        model.last_name = entity.last_name
        model.email = entity.email
        model.is_active = entity.is_active

        if entity.roles is not None:
            role_models = (
                self._session.query(RoleModel)
                .filter(RoleModel.name.in_(entity.roles))
                .all()
            )
            model.roles = role_models

        self._session.commit()
        self._session.refresh(model)

        return self._mapper.to_entity(model)

from typing import Optional

from sqlalchemy.orm import Session

from src.core.domain.entities.user import User
from src.core.infrastructure.mappers import UserMapper
from src.core.infrastructure.models import UserModel
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

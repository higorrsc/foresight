from typing import Generic, List, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.domain._shared.repository import AbstractRepository

T = TypeVar("T")
M = TypeVar("M")


class SQLAlchemyRepository(AbstractRepository[T], Generic[T, M]):
    """
    SQLAlchemy implementation of the AbstractRepository.
    Works with any database supported by SQLAlchemy.
    """

    def __init__(self, session: Session, model_cls: Type[M], mapper):
        """
        Initialize the repository.

        :param session: SQLAlchemy session.
        :param model_cls: SQLAlchemy model class (e.g., AreaModel).
        :param mapper: Mapper with to_model(entity) and to_entity(model).
        """

        self._session = session
        self._model_cls = model_cls
        self._mapper = mapper

    def save(self, entity: T) -> Optional[T]:
        """
        Save an entity to the repository.

        :param entity: The entity to be saved.
        :return: The saved entity.
        """

        model = self._mapper.to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._mapper.to_entity(model)

    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :return: The entity if found, otherwise None.
        """

        model = self._session.get(self._model_cls, entity_id)
        return self._mapper.to_entity(model) if model else None

    def list(self) -> List[T]:
        """
        List all entities in the repository.

        :return: A list of all entities.
        """

        models = self._session.query(self._model_cls).all()
        return [self._mapper.to_entity(m) for m in models]

    def update(self, entity: T) -> Optional[T]:
        """
        Update an existing entity in the repository.

        :param entity: The entity to be updated.
        :return: The updated entity.
        """

        model = self._mapper.to_model(entity)
        merged_model = self._session.merge(model)
        self._session.commit()
        self._session.refresh(merged_model)
        return self._mapper.to_entity(merged_model)

    def delete(self, entity_id: UUID) -> None:
        """
        Delete an entity from the repository.

        :param entity_id: The ID of the entity to be deleted.
        """

        model = self._session.get(self._model_cls, entity_id)

        if model:
            self._session.delete(model)
            self._session.commit()

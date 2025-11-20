from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import asc, delete, desc, func, inspect, select  # Adicionado func
from sqlalchemy.orm import Session

from src.shared_kernel.domain._shared import AbstractRepository, PaginatedResult

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

    def _has_column(self, column_name: str) -> bool:
        """
        Check if a column exists in the model.
        """

        mapper = inspect(self._model_cls)
        return column_name in mapper.columns  # type: ignore

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

    def get_by_id(
        self,
        entity_id: UUID,
        tenant_id: Optional[UUID],
    ) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :param tenant_id: The ID of the tenant.
        :return: The entity if found, otherwise None.
        """

        stmt = select(self._model_cls).where(self._model_cls.id == entity_id)  # type: ignore

        if self._has_column("tenant_id"):
            stmt = stmt.where(getattr(self._model_cls, "tenant_id") == tenant_id)

        model = self._session.scalars(stmt).first()
        return self._mapper.to_entity(model) if model else None

    def list(
        self,
        tenant_id: Optional[UUID],
    ) -> List[T]:
        """
        List all entities in the repository.

        :param tenant_id: The ID of the tenant.
        :return: A list of all entities.
        """

        stmt = select(self._model_cls)

        if self._has_column("tenant_id"):
            stmt = stmt.filter_by(tenant_id=tenant_id)

        result = self._session.execute(stmt)
        return [self._mapper.to_entity(m) for m in result.unique().scalars().all()]

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

    def delete(
        self,
        entity_id: UUID,
        tenant_id: Optional[UUID],
    ) -> None:
        """
        Delete an entity from the repository.

        :param entity_id: The ID of the entity to be deleted.
        :param tenant_id: The ID of the tenant.
        """

        stmt = delete(self._model_cls).where(self._model_cls.id == entity_id)  # type: ignore

        if self._has_column("tenant_id"):
            stmt = stmt.where(getattr(self._model_cls, "tenant_id") == tenant_id)

        self._session.execute(stmt)  # type: ignore
        self._session.commit()

    def search(
        self,
        tenant_id: Optional[UUID],
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        offset: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
    ) -> PaginatedResult[T]:
        """
        Search for entities based on criteria, with sorting and pagination.
        """

        stmt = select(self._model_cls)

        if self._has_column("tenant_id"):
            stmt = stmt.filter_by(tenant_id=tenant_id)

        if not include_inactive and self._has_column("is_active"):
            stmt = stmt.filter_by(is_active=True)  # type: ignore  # noqa: E712

        if filters:
            for field, value in filters.items():
                if hasattr(self._model_cls, field):
                    stmt = stmt.filter(
                        getattr(self._model_cls, field).ilike(f"%{value}%")
                    )

        count_stmt = stmt.with_only_columns(func.count()).order_by(None)
        total = self._session.scalar(count_stmt) or 0

        if sort_by and hasattr(self._model_cls, sort_by):
            column = getattr(self._model_cls, sort_by)
            if sort_order.lower() == "desc":
                stmt = stmt.order_by(desc(column))
            else:
                stmt = stmt.order_by(asc(column))

        stmt = stmt.offset(offset).limit(limit)

        result = self._session.execute(stmt)
        unique_results = result.unique()
        models = unique_results.scalars().all()
        entities = [self._mapper.to_entity(model) for model in models]

        return PaginatedResult(
            data=entities,
            total=total,
        )

from typing import Any
from uuid import UUID

from sqlalchemy import asc, delete, desc, func, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain import AbstractRepository, PaginatedResult
from src.core.infrastructure.mappers.mapper import AbstractMapper


class SQLAlchemyRepository[T, M](AbstractRepository[T]):
    """
    SQLAlchemy implementation of the AbstractRepository.
    Works with any database supported by SQLAlchemy.
    """

    def __init__(
        self, session: AsyncSession, model_cls: type[M], mapper: AbstractMapper[T, M]
    ):
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
        return column_name in mapper.columns.keys()  # type: ignore

    def _get_column(self, column_name: str):
        """
        Get a column from the model.
        """

        return getattr(self._model_cls, column_name, None)

    def _get_base_query(self):
        """Hook to allow children repos add eager loads (options)."""

        return select(self._model_cls)

    async def save(self, entity: T) -> T | None:
        """
        Save an entity to the repository.

        :param entity: The entity to be saved.
        :return: The saved entity.
        """

        model = self._mapper.to_model(entity)
        self._session.add(model)
        await self._session.flush()
        return self._mapper.to_entity(model)

    async def get_by_id(
        self,
        entity_id: UUID,
        tenant_id: UUID | None,
    ) -> T | None:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :param tenant_id: The ID of the tenant.
        :return: The entity if found, otherwise None.
        """

        id_column = self._get_column("id")
        if id_column is None:
            return None

        stmt = self._get_base_query().where(id_column == entity_id)

        tenant_column = self._get_column("tenant_id")
        if tenant_column is not None:
            stmt = stmt.where(tenant_column == tenant_id)

        result = await self._session.execute(stmt)
        model = result.unique().scalars().first()
        return self._mapper.to_entity(model) if model else None

    async def get_all(
        self,
        tenant_id: UUID | None,
    ) -> list[T]:
        """
        List all entities in the repository.

        :param tenant_id: The ID of the tenant.
        :return: A list of all entities.
        """

        stmt = self._get_base_query()

        tenant_column = self._get_column("tenant_id")
        if tenant_column is not None:
            stmt = stmt.where(tenant_column == tenant_id)

        result = await self._session.execute(stmt)
        models = result.unique().unique().scalars().all()
        return [self._mapper.to_entity(m) for m in models]

    async def update(self, entity: T) -> T | None:
        """
        Update an existing entity in the repository.

        :param entity: The entity to be updated.
        :return: The updated entity.
        """

        id_column = self._get_column("id")
        if id_column is None or not hasattr(entity, "id"):
            return None

        stmt = self._get_base_query().where(id_column == entity.id)  # type:ignore

        tenant_column = self._get_column("tenant_id")
        if tenant_column is not None and hasattr(entity, "tenant_id"):
            stmt = stmt.where(tenant_column == entity.tenant_id)  # type:ignore

        result = await self._session.execute(stmt)
        existing_model = result.unique().scalar_one_or_none()

        if not existing_model:
            return None

        updated_model = self._mapper.to_model(entity)

        mapper_info = inspect(self._model_cls)
        for column in mapper_info.columns:  # type: ignore
            col_name = column.name
            if hasattr(updated_model, col_name):
                setattr(existing_model, col_name, getattr(updated_model, col_name))

        await self._session.flush()
        return self._mapper.to_entity(existing_model)

    async def delete(
        self,
        entity_id: UUID,
        tenant_id: UUID | None,
    ) -> None:
        """
        Delete an entity from the repository.

        :param entity_id: The ID of the entity to be deleted.
        :param tenant_id: The ID of the tenant.
        """

        id_column = self._get_column("id")
        if id_column is None:
            return

        stmt = delete(self._model_cls).where(id_column == entity_id)

        tenant_column = self._get_column("tenant_id")
        if tenant_column is not None:
            stmt = stmt.where(tenant_column == tenant_id)

        await self._session.execute(stmt)
        await self._session.flush()

    async def search(
        self,
        tenant_id: UUID | None,
        filters: dict[str, Any] | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
        offset: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
    ) -> PaginatedResult[T]:
        """
        Search for entities based on criteria, with sorting and pagination.
        """

        stmt = self._get_base_query()

        tenant_column = self._get_column("tenant_id")
        if tenant_column is not None:
            stmt = stmt.where(tenant_column == tenant_id)

        is_active_column = self._get_column("is_active")
        if not include_inactive and is_active_column is not None:
            stmt = stmt.where(is_active_column.is_(True))

        if filters:
            for field, value in filters.items():
                column = self._get_column(field)
                if column is not None:
                    stmt = stmt.where(column.ilike(f"%{value}%"))

        count_stmt = select(func.count()).select_from(stmt.subquery())  # type: ignore
        total = await self._session.scalar(count_stmt) or 0

        if sort_by:
            column = self._get_column(sort_by)
            if column is not None:
                stmt = stmt.order_by(
                    desc(column) if sort_order.lower() == "desc" else asc(column)
                )

        stmt = stmt.offset(offset).limit(limit)

        result = await self._session.execute(stmt)
        models = result.unique().unique().scalars().all()
        entities = [self._mapper.to_entity(model) for model in models]

        return PaginatedResult(
            data=entities,
            total=total,
        )

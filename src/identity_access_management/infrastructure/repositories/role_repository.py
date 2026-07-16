from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.repositories import IRoleRepository
from src.identity_access_management.infrastructure.mappers import RoleMapper
from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    RoleModel,
)


class RoleRepository(
    SQLAlchemyRepository[Role, RoleModel],
    IRoleRepository,
):
    """
    Repository for managing Role entities using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the RoleRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(
            session,
            RoleModel,
            RoleMapper(),
        )

    def _get_base_query(self):
        """Overwrites the base query to always load permissions of the role."""

        return select(self._model_cls).options(
            selectinload(self._model_cls.permissions_rel)
        )

    async def get_by_id(
        self,
        entity_id: UUID,
        tenant_id: UUID | None,
    ) -> Role | None:
        """Get a role by its ID, ensuring permissions are loaded."""

        stmt = self._get_base_query().where(
            self._model_cls.id == entity_id,
            self._model_cls.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return self._mapper.to_entity(model) if model else None

    async def get_by_name(
        self,
        name: str,
        tenant_id: UUID | None,
    ) -> Role | None:
        """
        Get a role by its name.
        """

        stmt = self._get_base_query().where(
            self._model_cls.name == name,
            self._model_cls.tenant_id == tenant_id,
        )

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return self._mapper.to_entity(model) if model else None

    async def save(self, entity: Role) -> Role | None:
        """
        Save Role entity
        """

        model = self._mapper.to_model(entity)
        if entity.permissions:
            stmt = select(PermissionModel).where(
                PermissionModel.codename.in_(entity.permissions)
            )

            result = await self._session.execute(stmt)
            permissions_model = list(result.unique().scalars().all())
            model.permissions_rel = permissions_model
        else:
            model.permissions_rel = []

        self._session.add(model)
        await self._session.flush()

        return self._mapper.to_entity(model)

    async def update(self, entity: Role) -> Role | None:
        """
        Update Role entity
        """

        stmt = self._get_base_query().where(self._model_cls.id == entity.id)
        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        if not model:
            return None

        model.name = entity.name  # type:ignore
        model.description = entity.description  # type:ignore
        model.is_active = entity.is_active

        if hasattr(entity, "deleted_at"):
            model.deleted_at = entity.deleted_at

        if entity.permissions:
            stmt = select(PermissionModel).where(
                PermissionModel.codename.in_(entity.permissions)
            )

            result = await self._session.execute(stmt)
            permission_models = list(result.unique().scalars().all())

            model.permissions_rel = permission_models

        await self._session.flush()

        return self._mapper.to_entity(model)

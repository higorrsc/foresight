from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.repositories import IUserRepository
from src.identity_access_management.infrastructure.mappers import UserMapper
from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    RoleModel,
    UserModel,
)


class UserRepository(
    SQLAlchemyRepository[User, UserModel],
    IUserRepository,
):
    """
    Repository for managing User entities using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the UserRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(
            session,
            UserModel,
            UserMapper(),
        )

    def _get_base_query(self):
        """Overwrites the base query to always load permissions and roles."""

        return select(self._model_cls).options(
            selectinload(self._model_cls.permissions_rel),
            selectinload(self._model_cls.roles_rel).selectinload(
                RoleModel.permissions_rel
            ),
        )

    async def get_by_id(
        self,
        entity_id: UUID,
        tenant_id: UUID | None,
    ) -> User | None:
        """Get a role by its ID, ensuring permissions are loaded."""

        stmt = self._get_base_query().where(
            self._model_cls.id == entity_id,
            self._model_cls.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return self._mapper.to_entity(model) if model else None

    async def get_by_username(
        self,
        username: str,
        tenant_id: UUID | None,
    ) -> User | None:
        """
        Get a user by its username and tenant.
        """

        stmt = self._get_base_query().where(
            self._model_cls.username == username,
            self._model_cls.tenant_id == tenant_id,
        )

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return self._mapper.to_entity(model) if model else None

    async def get_by_email(
        self,
        email: str,
        tenant_id: UUID | None,
    ) -> User | None:
        """
        Get a user by its email.

        :param email: Email of the user.
        :return: User entity or None if not found.
        """

        stmt = self._get_base_query().where(
            self._model_cls.email == email,
            self._model_cls.tenant_id == tenant_id,
        )

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return self._mapper.to_entity(model) if model else None

    async def get_by_username_global(self, username: str) -> User | None:
        """
        Get a user by its username at any tenant.

        :param username: Username of the user.
        :return: User entity or None if not found.
        """

        stmt = self._get_base_query().where(self._model_cls.username == username)

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return self._mapper.to_entity(model) if model else None

    async def save(self, entity: User) -> User | None:
        """
        Save User entity
        """

        model = self._mapper.to_model(entity)

        if entity.roles:
            stmt = (
                select(RoleModel)
                .options(selectinload(RoleModel.permissions_rel))
                .where(RoleModel.name.in_(entity.roles))
            )
            result = await self._session.execute(stmt)
            role_models = list(result.unique().scalars().all())
            model.roles_rel = role_models
        else:
            model.roles_rel = []

        if not hasattr(model, "permissions_rel") or model.permissions_rel is None:
            model.permissions_rel = []

        self._session.add(model)
        await self._session.flush()

        return self._mapper.to_entity(model)

    async def update(self, entity: User) -> User | None:
        """
        Update User entity
        """

        stmt = self._get_base_query().where(self._model_cls.id == entity.id)
        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        if not model:
            return None

        model.username = entity.username  # type:ignore
        model.hashed_password = entity.hashed_password  # type:ignore
        model.first_name = entity.first_name  # type:ignore
        model.last_name = entity.last_name  # type:ignore
        model.email = entity.email  # type:ignore
        model.is_active = entity.is_active

        if hasattr(entity, "deleted_at"):
            model.deleted_at = entity.deleted_at

        if entity.roles is not None:
            stmt = (
                select(RoleModel)
                .options(selectinload(RoleModel.permissions_rel))
                .where(RoleModel.name.in_(entity.roles))
            )
            result = await self._session.execute(stmt)
            role_models = list(result.unique().scalars().all())
            model.roles_rel = role_models

        if entity.permissions is not None:
            stmt = select(PermissionModel).where(  # type:ignore
                PermissionModel.codename.in_(entity.permissions)
            )
            result = await self._session.execute(stmt)
            permission_models = list(result.unique().scalars().all())
            model.permissions_rel = permission_models

        await self._session.flush()

        return self._mapper.to_entity(model)

    async def count_users_by_role(self, role_id: UUID) -> int:
        """
        Count the number of users associated with a role.
        """

        stmt = (
            select(func.count(UserModel.id))  # type:ignore
            .join(UserModel.roles_rel)
            .where(RoleModel.id == role_id)
        )

        result = await self._session.execute(stmt)

        return result.scalar_one()

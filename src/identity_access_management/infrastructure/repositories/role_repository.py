from uuid import UUID

from sqlalchemy.orm import Session

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

    def __init__(self, session: Session):
        """
        Initialize the RoleRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, RoleModel, RoleMapper())

    def get_by_name(
        self,
        name: str,
        tenant_id: UUID | None,
    ) -> Role | None:
        """
        Get a role by its name.
        """

        model = (
            self._session.query(self._model_cls)
            .filter_by(name=name, tenant_id=tenant_id)
            .first()
        )
        return self._mapper.to_entity(model) if model else None

    def save(self, entity: Role) -> Role | None:
        """
        Save Role entity
        """

        model = self._mapper.to_model(entity)
        if entity.permissions:
            permissions_model = (
                self._session.query(PermissionModel)
                .filter(PermissionModel.codename.in_(entity.permissions))
                .all()
            )
            model.permissions_rel = permissions_model

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)

        return self._mapper.to_entity(model)

    def update(self, entity: Role) -> Role | None:
        """
        Update Role entity
        """

        model = self._session.get(self._model_cls, entity.id)
        if not model:
            return None

        model.name = entity.name  # type: ignore
        model.description = entity.description  # type: ignore
        model.is_active = entity.is_active  # type: ignore

        if hasattr(entity, "deleted_at"):
            model.deleted_at = entity.deleted_at  # type: ignore

        if entity.permissions:
            permission_models = (
                self._session.query(PermissionModel)
                .filter(PermissionModel.codename.in_(entity.permissions))
                .all()
            )
            model.permissions_rel = permission_models

        self._session.commit()
        self._session.refresh(model)

        return self._mapper.to_entity(model)

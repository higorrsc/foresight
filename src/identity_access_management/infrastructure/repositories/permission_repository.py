from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.identity_access_management.domain.entities import Permission
from src.identity_access_management.domain.repositories import IPermissionRepository
from src.identity_access_management.infrastructure.mappers import PermissionMapper
from src.identity_access_management.infrastructure.models import PermissionModel


class PermissionRepository(
    SQLAlchemyRepository[Permission, PermissionModel],
    IPermissionRepository,
):
    """
    Concrete implementation of the Permission repository using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the PermissionRepository with a SQLAlchemy session.
        """

        super().__init__(
            session=session,
            model_cls=PermissionModel,
            mapper=PermissionMapper,
        )

    def list_all(self) -> list[Permission]:
        """
        Lists all permissions.
        """

        stmt = select(self._model_cls)
        models = self._session.scalars(stmt).all()
        return [self._mapper.to_entity(m) for m in models]

    def get_by_codename(self, codename: str) -> Permission | None:
        """
        Retrieves a permission by its codename.
        """

        stmt = select(self._model_cls).filter_by(codename=codename)
        model = self._session.scalars(stmt).first()
        return self._mapper.to_entity(model) if model else None

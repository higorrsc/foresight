from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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

    def __init__(self, session: AsyncSession):
        """
        Initialize the PermissionRepository with a SQLAlchemy session.
        """

        super().__init__(
            session,
            PermissionModel,
            PermissionMapper(),
        )

    async def list_all(self) -> list[Permission]:
        """
        Lists all permissions.
        """

        stmt = select(self._model_cls)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._mapper.to_entity(m) for m in models]

    async def get_by_codename(self, codename: str) -> Permission | None:
        """
        Retrieves a permission by its codename.
        """

        stmt = select(self._model_cls).filter_by(codename=codename)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_entity(model) if model else None

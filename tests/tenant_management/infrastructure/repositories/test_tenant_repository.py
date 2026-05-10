from unittest.mock import AsyncMock, patch
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.tenant_management.domain.entities import Tenant
from src.tenant_management.infrastructure.mappers import TenantMapper
from src.tenant_management.infrastructure.models import TenantModel
from src.tenant_management.infrastructure.repositories import TenantRepository


class TestTenantRepository:
    """
    Test suite for the TenantRepository.
    """

    async def test_save_tenant(self, mock_tenant_entity: Tenant) -> None:
        """
        Should correctly map an entity to a model and add it to the session.
        """

        mock_session = AsyncMock(spec=AsyncSession)  # AsyncSession
        mock_tenant_model = AsyncMock(spec=TenantModel)

        mock_tenant_model.id = mock_tenant_entity.id
        mock_tenant_model.name = mock_tenant_entity.name
        mock_tenant_model.plan_id = mock_tenant_entity.plan_id
        mock_tenant_model.status = mock_tenant_entity.status.value

        with patch.object(
            TenantMapper,
            "to_model",
            return_value=mock_tenant_model,
        ) as mock_to_model:
            with patch.object(
                TenantMapper, "to_entity", return_value=mock_tenant_entity
            ):
                repository = TenantRepository(session=mock_session)
                await repository.save(mock_tenant_entity)
                mock_to_model.assert_called_once_with(mock_tenant_entity)
                mock_session.add.assert_called_once_with(mock_tenant_model)

    async def test_get_by_id_found(self) -> None:
        """
        Should return a Tenant entity when a tenant with the given id exists.
        """

        mock_session = AsyncMock(spec=AsyncSession)
        mock_tenant_model = AsyncMock(spec=TenantModel)
        mock_tenant_entity = AsyncMock(spec=Tenant)
        tenant_id = uuid4()

        # If get_by_id_global uses session.get:
        mock_session.get = AsyncMock(return_value=mock_tenant_model)

        mock_session.get.return_value = mock_tenant_model
        with patch.object(
            TenantMapper,
            "to_entity",
            return_value=mock_tenant_entity,
        ) as mock_to_entity:
            repository = TenantRepository(session=mock_session)

            result = await repository.get_by_id_global(tenant_id)

            mock_to_entity.assert_called_once_with(mock_tenant_model)
            assert result == mock_tenant_entity

    async def test_get_by_id_not_found(self) -> None:
        """
        Should return None when no tenant with the given id exists.
        """

        mock_session = AsyncMock(spec=AsyncSession)
        tenant_id = uuid4()

        # The overridden get_by_id calls session.get
        mock_session.get.return_value = None

        with patch.object(TenantMapper, "to_entity") as mock_to_entity:
            repository = TenantRepository(session=mock_session)

            result = await repository.get_by_id_global(tenant_id)

            mock_to_entity.assert_not_called()
            assert result is None

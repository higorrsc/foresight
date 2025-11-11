from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from src.tenant_management.domain.entities.tenant import Tenant
from src.tenant_management.domain.value_objects import TenantStatus
from src.tenant_management.infrastructure.mappers.tenant_mapper import TenantMapper
from src.tenant_management.infrastructure.models.tenant_model import TenantModel
from src.tenant_management.infrastructure.repositories.tenant_repository import (
    TenantRepository,
)


class TestTenantRepository:
    """
    Test suite for the TenantRepository.
    """

    @pytest.fixture
    def mock_tenant_entity(self) -> Tenant:
        """Provides a valid Tenant entity mock for tests."""
        tenant = Mock(spec=Tenant)
        tenant.id = uuid4()
        tenant.name = "Test Tenant"
        tenant.plan_id = uuid4()
        tenant.status = TenantStatus.ACTIVE
        return tenant

    def test_save_tenant(self, mock_tenant_entity: Tenant) -> None:
        """
        Should correctly map an entity to a model and add it to the session.
        """

        mock_session = Mock(spec=Session)
        mock_tenant_model = Mock(spec=TenantModel)
        # Configure the mock model with real data to avoid validation errors on return
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
                repository.save(mock_tenant_entity)
                mock_to_model.assert_called_once_with(mock_tenant_entity)
                mock_session.add.assert_called_once_with(mock_tenant_model)

    def test_get_by_id_found(self) -> None:
        """
        Should return a Tenant entity when a tenant with the given id exists.
        """

        mock_session = Mock(spec=Session)
        mock_tenant_model = Mock(spec=TenantModel)
        mock_tenant_entity = Mock(spec=Tenant)
        tenant_id = uuid4()

        mock_session.get.return_value = mock_tenant_model
        with patch.object(
            TenantMapper,
            "to_entity",
            return_value=mock_tenant_entity,
        ) as mock_to_entity:
            repository = TenantRepository(session=mock_session)

            result = repository.get_by_id_global(tenant_id)

            # The overridden get_by_id calls session.get
            mock_session.get.assert_called_once_with(repository._model_cls, tenant_id)
            mock_to_entity.assert_called_once_with(mock_tenant_model)
            assert result == mock_tenant_entity

    def test_get_by_id_not_found(self) -> None:
        """
        Should return None when no tenant with the given id exists.
        """

        mock_session = Mock(spec=Session)
        tenant_id = uuid4()

        # The overridden get_by_id calls session.get
        mock_session.get.return_value = None

        with patch.object(TenantMapper, "to_entity") as mock_to_entity:
            repository = TenantRepository(session=mock_session)

            result = repository.get_by_id_global(tenant_id)

            mock_session.get.assert_called_once_with(repository._model_cls, tenant_id)
            mock_to_entity.assert_not_called()
            assert result is None

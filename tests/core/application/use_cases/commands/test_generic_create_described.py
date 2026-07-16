from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.core.application.use_cases.commands import (
    CreateDescribedEntityInputDTO,
    CreateDescribedEntityUseCase,
)
from src.core.domain.entities import DescribedEntity
from src.identity_access_management.domain.exceptions import InsufficientPermissionError


class MockEntity(DescribedEntity):
    """
    A mock entity for testing purposes.
    """


class TestCreateDescribedEntityUseCase:
    """
    Test suite for the CreateDescribedEntityUseCase.
    """

    async def test_execute_success(self):
        """
        Test successful execution of the create described entity use case.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = {"test:create"}
        actor.tenant_id = uuid4()

        use_case = CreateDescribedEntityUseCase(
            repository=repository,
            required_permission="test:create",  # type: ignore
            entity_cls=MockEntity,
            invalid_data_exception=ValueError,
        )

        input_dto = CreateDescribedEntityInputDTO(
            actor=actor,
            description="Test description",
        )

        output = await use_case.execute(input_dto)

        assert output.id is not None
        assert repository.save.called
        saved_entity = repository.save.call_args[0][0]
        assert isinstance(saved_entity, MockEntity)
        assert saved_entity.description == "Test description"
        assert saved_entity.tenant_id == actor.tenant_id

    async def test_execute_insufficient_permission(self):
        """
        Test that execution fails when the actor has insufficient permissions.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = {"other:permission"}

        use_case = CreateDescribedEntityUseCase(
            repository=repository,
            required_permission="test:create",  # type: ignore
            entity_cls=MockEntity,
            invalid_data_exception=ValueError,
        )

        input_dto = CreateDescribedEntityInputDTO(
            actor=actor,
            description="Test description",
        )

        with pytest.raises(InsufficientPermissionError):
            await use_case.execute(input_dto)

    async def test_execute_invalid_data(self):
        """
        Test that execution fails when provided with invalid data.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = {"test:create"}

        use_case = CreateDescribedEntityUseCase(
            repository=repository,
            required_permission="test:create",  # type: ignore
            entity_cls=MockEntity,
            invalid_data_exception=ValueError,
        )

        # Empty description should trigger EntityValidationError in DescribedEntity
        input_dto = CreateDescribedEntityInputDTO(
            actor=actor,
            description="",
        )

        with pytest.raises(ValueError) as excinfo:
            await use_case.execute(input_dto)

        assert "Invalid input data" in str(excinfo.value)

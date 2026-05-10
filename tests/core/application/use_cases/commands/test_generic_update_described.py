from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_update_described import (
    UpdateDescribedEntityInputDTO,
    UpdateDescribedEntityUseCase,
)
from src.core.domain.entities import DescribedEntity
from src.identity_access_management.domain.exceptions import InsufficientPermissionError


class MockEntity(DescribedEntity):
    """
    A mock entity for testing purposes.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updated_by = None


class TestUpdateDescribedEntityUseCase:
    """
    Test suite for the UpdateDescribedEntityUseCase.
    """

    async def test_execute_success(self):
        """
        Test successful update of a described entity.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = {"test:update"}
        actor.tenant_id = uuid4()
        actor.id = uuid4()

        entity = MockEntity(
            id=uuid4(), description="Old description", tenant_id=actor.tenant_id
        )
        repository.get_by_id.return_value = entity

        use_case = UpdateDescribedEntityUseCase(
            repository=repository,
            required_permission="test:update",  # type: ignore
            not_found_exception=ValueError,
            invalid_data_exception=TypeError,
        )

        input_dto = UpdateDescribedEntityInputDTO(
            actor=actor,
            id=entity.id,
            description="New description",
        )

        output = await use_case.execute(input_dto)

        assert output.description == "New description"
        assert entity.description == "New description"
        assert entity.updated_by == actor.id
        assert repository.update.called

    async def test_execute_insufficient_permission(self):
        """
        Test that update fails when the actor has insufficient permissions.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = set()

        use_case = UpdateDescribedEntityUseCase(
            repository=repository,
            required_permission="test:update",  # type: ignore
            not_found_exception=ValueError,
            invalid_data_exception=TypeError,
        )

        input_dto = UpdateDescribedEntityInputDTO(
            actor=actor,
            id=uuid4(),
            description="New description",
        )

        with pytest.raises(InsufficientPermissionError):
            await use_case.execute(input_dto)

    async def test_execute_not_found(self):
        """
        Test that update fails when the entity is not found.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = {"test:update"}
        actor.tenant_id = uuid4()
        repository.get_by_id.return_value = None

        use_case = UpdateDescribedEntityUseCase(
            repository=repository,
            required_permission="test:update",  # type: ignore
            not_found_exception=ValueError,
            invalid_data_exception=TypeError,
        )

        entity_id = uuid4()
        input_dto = UpdateDescribedEntityInputDTO(
            actor=actor,
            id=entity_id,
            description="New description",
        )

        with pytest.raises(ValueError) as excinfo:
            await use_case.execute(input_dto)
        assert f"Entity with id {entity_id} not found" in str(excinfo.value)

    async def test_execute_invalid_data(self):
        """
        Test that update fails when provided with invalid data.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = {"test:update"}
        actor.tenant_id = uuid4()

        entity = MockEntity(
            id=uuid4(), description="Old description", tenant_id=actor.tenant_id
        )
        repository.get_by_id.return_value = entity

        use_case = UpdateDescribedEntityUseCase(
            repository=repository,
            required_permission="test:update",  # type: ignore
            not_found_exception=ValueError,
            invalid_data_exception=TypeError,
        )

        input_dto = UpdateDescribedEntityInputDTO(
            actor=actor,
            id=entity.id,
            description="",  # Invalid
        )

        with pytest.raises(TypeError) as excinfo:
            await use_case.execute(input_dto)
        assert "Invalid input data" in str(excinfo.value)

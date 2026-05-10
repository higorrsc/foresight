from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_restore import (
    GenericRestoreUseCase,
    RestoreRequestInputDTO,
)
from src.core.domain.mixins import SoftDeletableMixin
from src.identity_access_management.domain.exceptions import InsufficientPermissionError


class MockSoftDeletableEntity(SoftDeletableMixin):
    """
    A mock entity that implements SoftDeletableMixin for testing purposes.
    """

    def __init__(self):
        self.id = uuid4()
        self.updated_by = None
        super().__init__()


class TestGenericRestoreUseCase:
    """
    Test suite for the GenericRestoreUseCase.
    """

    async def test_execute_success(self):
        """
        Test successful restoration of a soft-deleted entity.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = {"test:restore"}
        actor.tenant_id = uuid4()
        actor.id = uuid4()

        entity = MockSoftDeletableEntity()
        entity.soft_delete()
        repository.get_by_id.return_value = entity

        use_case = GenericRestoreUseCase(
            repository=repository,
            required_permission="test:restore",  # type: ignore
            not_found_exception=ValueError,
        )

        input_dto = RestoreRequestInputDTO(
            actor=actor,
            id=entity.id,
        )

        await use_case.execute(input_dto)

        assert entity.is_active is True
        assert entity.deleted_at is None
        assert entity.updated_by == actor.id
        assert repository.update.called

    async def test_execute_insufficient_permission(self):
        """
        Test that restoration fails when the actor has insufficient permissions.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = set()

        use_case = GenericRestoreUseCase(
            repository=repository,
            required_permission="test:restore",  # type: ignore
            not_found_exception=ValueError,
        )

        input_dto = RestoreRequestInputDTO(
            actor=actor,
            id=uuid4(),
        )

        with pytest.raises(InsufficientPermissionError):
            await use_case.execute(input_dto)

    async def test_execute_not_found(self):
        """
        Test that restoration fails when the entity is not found.
        """
        repository = AsyncMock()
        actor = AsyncMock()
        actor.permissions = {"test:restore"}
        actor.tenant_id = uuid4()
        repository.get_by_id.return_value = None

        use_case = GenericRestoreUseCase(
            repository=repository,
            required_permission="test:restore",  # type: ignore
            not_found_exception=ValueError,
            not_found_message="Not found {id}",
        )

        entity_id = uuid4()
        input_dto = RestoreRequestInputDTO(
            actor=actor,
            id=entity_id,
        )

        with pytest.raises(ValueError) as excinfo:
            await use_case.execute(input_dto)
        assert f"Not found {entity_id}" in str(excinfo.value)

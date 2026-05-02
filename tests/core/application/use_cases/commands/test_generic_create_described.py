from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_create_described import (
    CreateDescribedEntityInputDTO,
    CreateDescribedEntityUseCase,
)
from src.core.domain.entities.described import DescribedEntity
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)


class MockEntity(DescribedEntity):
    """
    A mock entity for testing purposes.
    """

    pass


class TestCreateDescribedEntityUseCase:
    """
    Test suite for the CreateDescribedEntityUseCase.
    """

    def test_execute_success(self):
        """
        Test successful execution of the create described entity use case.
        """
        repository = MagicMock()
        actor = MagicMock()
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

        output = use_case.execute(input_dto)

        assert output.id is not None
        assert repository.save.called
        saved_entity = repository.save.call_args[0][0]
        assert isinstance(saved_entity, MockEntity)
        assert saved_entity.description == "Test description"
        assert saved_entity.tenant_id == actor.tenant_id

    def test_execute_insufficient_permission(self):
        """
        Test that execution fails when the actor has insufficient permissions.
        """
        repository = MagicMock()
        actor = MagicMock()
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
            use_case.execute(input_dto)

    def test_execute_invalid_data(self):
        """
        Test that execution fails when provided with invalid data.
        """
        repository = MagicMock()
        actor = MagicMock()
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
            use_case.execute(input_dto)
        assert "Invalid input data" in str(excinfo.value)

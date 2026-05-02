from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_update_described import (
    UpdateDescribedEntityInputDTO,
    UpdateDescribedEntityUseCase,
)
from src.core.domain.entities.described import DescribedEntity
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)


class MockEntity(DescribedEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updated_by = None


class TestUpdateDescribedEntityUseCase:
    def test_execute_success(self):
        repository = MagicMock()
        actor = MagicMock()
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

        output = use_case.execute(input_dto)

        assert output.description == "New description"
        assert entity.description == "New description"
        assert entity.updated_by == actor.id
        assert repository.update.called

    def test_execute_insufficient_permission(self):
        repository = MagicMock()
        actor = MagicMock()
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
            use_case.execute(input_dto)

    def test_execute_not_found(self):
        repository = MagicMock()
        actor = MagicMock()
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
            use_case.execute(input_dto)
        assert f"Entity with id {entity_id} not found" in str(excinfo.value)

    def test_execute_invalid_data(self):
        repository = MagicMock()
        actor = MagicMock()
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
            use_case.execute(input_dto)
        assert "Invalid input data" in str(excinfo.value)

from uuid import UUID

import pytest

from src.core.application.use_cases.commands import (
    DeleteRequestInputDTO,
    GenericDeleteUseCase,
)
from src.core.infrastructure.repository import InMemoryRepository
from tests.fakes import DummyEntity


class EntityNotFoundException(Exception):
    """
    Exception raised when an entity is not found in the repository.
    """


@pytest.fixture
def repository():
    """
    Fixture for an in-memory repository.
    """

    return InMemoryRepository()


@pytest.fixture
def delete_use_case(repository):
    """
    Fixture for a delete use case.
    """

    return GenericDeleteUseCase[DummyEntity](
        repository=repository,
        not_found_exception=EntityNotFoundException,
        not_found_message="DummyEntity with id={id} not found",
    )


class TestGenericDeleteUseCase:
    """
    Test suite for the GenericDeleteUseCase.
    """

    def test_delete_existing_entity(self, repository, delete_use_case, admin_actor):
        """
        Test deleting an existing entity.
        """

        entity = DummyEntity(
            name="Test Entity",
            tenant_id=admin_actor.tenant_id,
        )
        repository.save(entity)

        entity_id = DeleteRequestInputDTO(
            actor=admin_actor,
            id=entity.id,
        )
        delete_use_case.execute(request=entity_id)

        assert repository.get_by_id(entity_id, admin_actor.tenant_id) is None

    def test_delete_non_existing_entity_raises_exception(
        self, delete_use_case, admin_actor
    ):
        """
        Test deleting a non-existing entity raises the appropriate exception.
        """

        invalid_entity = DeleteRequestInputDTO(
            actor=admin_actor,
            id=UUID("c1c4d4d7-f545-5f27-b366-1546b022e622"),
        )

        with pytest.raises(EntityNotFoundException) as exc_info:
            delete_use_case.execute(request=invalid_entity)

        assert (
            str(exc_info.value) == f"DummyEntity with id={invalid_entity.id} not found"
        )

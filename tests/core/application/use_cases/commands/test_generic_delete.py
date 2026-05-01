from uuid import uuid4

import pytest

from src.core.application.use_cases.commands import (
    DeleteRequestInputDTO,
    GenericDeleteUseCase,
)
from src.core.domain import EntityNotFoundError
from src.core.infrastructure.repository import InMemoryRepository
from src.identity_access_management.domain.constants import AppPermission
from tests.fakes import DummyEntity


@pytest.fixture
def entity_id():
    """
    Fixture for an entity ID.
    """

    return uuid4()


@pytest.fixture
def repository():
    """
    Fixture for an in-memory repository.
    """

    return InMemoryRepository()


@pytest.fixture
def delete_use_case(repository, entity_id):
    """
    Fixture for a delete use case.
    """

    return GenericDeleteUseCase[DummyEntity](
        repository,
        AppPermission.USER_DELETE,
        EntityNotFoundError,
        f"DummyEntity with id={entity_id} not found",
    )


class TestGenericDeleteUseCase:
    """
    Test suite for the GenericDeleteUseCase.
    """

    def test_delete_existing_entity(
        self,
        repository,
        delete_use_case,
        admin_actor,
    ):
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
        self,
        delete_use_case,
        admin_actor,
        entity_id,
    ):
        """
        Test deleting a non-existing entity raises the appropriate exception.
        """

        invalid_entity = DeleteRequestInputDTO(
            actor=admin_actor,
            id=entity_id,
        )

        with pytest.raises(EntityNotFoundError) as exc_info:
            delete_use_case.execute(request=invalid_entity)

        assert str(exc_info.value) == f"DummyEntity with id={entity_id} not found"

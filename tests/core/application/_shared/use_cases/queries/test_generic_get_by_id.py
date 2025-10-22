from uuid import UUID

import pytest

from src.core.application._shared.use_cases.queries import (
    GenericGetByIdUseCase,
    GetByIdRequestInputDTO,
)
from src.core.domain._shared import EntityNotFoundException
from src.core.infrastructure.repositories._shared import InMemoryRepository
from tests.core.fakes import DummyEntity


@pytest.fixture
def repository():
    """
    Fixture for an in-memory repository.
    """

    return InMemoryRepository()


@pytest.fixture
def get_by_id_use_case(repository):
    """
    Fixture for a get by id use case.
    """

    return GenericGetByIdUseCase[DummyEntity](
        repository=repository,
        not_found_exception=EntityNotFoundException,
        not_found_message="DummyEntity with id={id} not found",
    )


class TestGenericGetByIdUseCase:
    """
    Test suite for the GenericGetByIdUseCase.
    """

    def test_get_by_id_existing_entity(self, repository, get_by_id_use_case):
        """
        Test getting an existing entity by ID.
        """

        entity = DummyEntity(name="Test Entity")
        repository.save(entity)

        request = GetByIdRequestInputDTO(id=entity.id)
        result = get_by_id_use_case.execute(request=request)

        assert result.id == entity.id
        assert result.name == entity.name  # type: ignore

    def test_get_by_id_non_existing_entity_raises_exception(self, get_by_id_use_case):
        """
        Test getting a non-existing entity by ID raises the appropriate exception.
        """

        invalid_id = UUID("c1c4d4d7-f545-5f27-b366-1546b022e622")
        request = GetByIdRequestInputDTO(id=invalid_id)

        with pytest.raises(EntityNotFoundException) as exc_info:
            get_by_id_use_case.execute(request=request)

        assert str(exc_info.value) == f"DummyEntity with id={invalid_id} not found"

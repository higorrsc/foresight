import pytest

from core.application._shared.use_cases.generic_list import GenericListUseCase
from core.tests.fakes import InMemoryRepository
from core.tests.fakes.dummy_entity import DummyEntity


@pytest.fixture
def repository():
    """
    Fixture for an in-memory repository.
    """

    return InMemoryRepository()


@pytest.fixture
def list_use_case(repository):
    """
    Fixture for a list use case.
    """

    return GenericListUseCase[DummyEntity](repository=repository)


class TestGenericListUseCase:
    """
    Test suite for the GenericListUseCase.
    """

    def test_list_entities(self, repository, list_use_case):
        """
        Test listing entities.
        """

        entity1 = DummyEntity(name="Entity 1")
        entity2 = DummyEntity(name="Entity 2")
        repository.save(entity1)
        repository.save(entity2)

        result = list_use_case.execute()

        assert len(result.data) == 2
        assert entity1 in result.data
        assert entity2 in result.data

    def test_list_no_entities(self, list_use_case):
        """
        Test listing when no entities are present.
        """

        result = list_use_case.execute()

        assert len(result.data) == 0

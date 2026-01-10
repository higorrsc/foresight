import pytest

from src.core.application.use_cases.queries import (
    GenericListUseCase,
    ListRequestInputDTO,
)
from src.shared_kernel.infrastructure.repositories._shared import InMemoryRepository
from tests.fakes import DummyEntity


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

    def test_list_entities(
        self,
        repository,
        list_use_case,
        admin_actor,
    ):
        """
        Test listing entities.
        """

        entity1 = DummyEntity(
            name="Entity 1",
            tenant_id=admin_actor.tenant_id,
        )
        entity2 = DummyEntity(
            name="Entity 2",
            tenant_id=admin_actor.tenant_id,
        )
        repository.save(entity1)
        repository.save(entity2)

        result = list_use_case.execute(ListRequestInputDTO(actor=admin_actor))

        assert len(result.data) == 2
        assert entity1 in result.data
        assert entity2 in result.data

    def test_list_no_entities(
        self,
        list_use_case,
        admin_actor,
    ):
        """
        Test listing when no entities are present.
        """

        result = list_use_case.execute(ListRequestInputDTO(actor=admin_actor))

        assert len(result.data) == 0

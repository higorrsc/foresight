from src.core.application.use_cases.queries import ListRequestInputDTO
from tests.fakes import DummyEntity


class TestGenericListUseCase:
    """
    Test suite for the GenericListUseCase.
    """

    def test_list_entities(
        self,
        dummy_in_memory_repository,
        generic_list_use_case,
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
        dummy_in_memory_repository.save(entity1)
        dummy_in_memory_repository.save(entity2)

        result = generic_list_use_case.execute(ListRequestInputDTO(actor=admin_actor))

        assert len(result.data) == 2
        assert entity1 in result.data
        assert entity2 in result.data

    def test_list_no_entities(
        self,
        generic_list_use_case,
        admin_actor,
    ):
        """
        Test listing when no entities are present.
        """

        result = generic_list_use_case.execute(ListRequestInputDTO(actor=admin_actor))

        assert len(result.data) == 0

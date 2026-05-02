import pytest

from src.core.application.use_cases.commands import DeleteRequestInputDTO
from src.core.domain import EntityNotFoundError
from tests.fakes import DummyEntity


class TestGenericDeleteUseCase:
    """
    Test suite for the GenericDeleteUseCase.
    """

    def test_delete_existing_entity(
        self,
        dummy_in_memory_repository,
        generic_delete_use_case,
        admin_actor,
    ):
        """
        Test deleting an existing entity.
        """

        entity = DummyEntity(
            name="Test Entity",
            tenant_id=admin_actor.tenant_id,
        )
        dummy_in_memory_repository.save(entity)

        request = DeleteRequestInputDTO(
            actor=admin_actor,
            id=entity.id,
        )
        generic_delete_use_case.execute(request=request)

        assert (
            dummy_in_memory_repository.get_by_id(entity.id, admin_actor.tenant_id)
            is None
        )

    def test_delete_non_existing_entity_raises_exception(
        self,
        generic_delete_use_case,
        admin_actor,
        generic_delete_entity_id,
    ):
        """
        Test deleting a non-existing entity raises the appropriate exception.
        """

        invalid_entity = DeleteRequestInputDTO(
            actor=admin_actor,
            id=generic_delete_entity_id,
        )

        with pytest.raises(EntityNotFoundError) as exc_info:
            generic_delete_use_case.execute(request=invalid_entity)

        assert (
            str(exc_info.value)
            == f"DummyEntity with id={generic_delete_entity_id} not found"
        )

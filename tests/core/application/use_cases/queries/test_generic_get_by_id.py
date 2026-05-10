from uuid import UUID

import pytest

from src.core.application.use_cases.queries import GetByIdRequestInputDTO
from src.core.domain import EntityNotFoundError
from tests.fakes import DummyEntity


class TestGenericGetByIdUseCase:
    """
    Test suite for the GenericGetByIdUseCase.
    """

    async def test_get_by_id_existing_entity(
        self,
        dummy_in_memory_repository,
        generic_get_by_id_use_case,
        admin_actor,
    ):
        """
        Test getting an existing entity by ID.
        """

        entity = DummyEntity(name="Test Entity", tenant_id=admin_actor.tenant_id)
        await dummy_in_memory_repository.save(entity)

        request = GetByIdRequestInputDTO(
            id=entity.id,
            actor=admin_actor,
        )
        result = await generic_get_by_id_use_case.execute(request=request)

        assert result.id == entity.id
        assert result.name == entity.name  # type: ignore

    async def test_get_by_id_non_existing_entity_raises_exception(
        self,
        generic_get_by_id_use_case,
        admin_actor,
    ):
        """
        Test getting a non-existing entity by ID raises the appropriate exception.
        """

        invalid_id = UUID("c1c4d4d7-f545-5f27-b366-1546b022e622")
        request = GetByIdRequestInputDTO(
            id=invalid_id,
            actor=admin_actor,
        )

        with pytest.raises(EntityNotFoundError) as exc_info:
            await generic_get_by_id_use_case.execute(request=request)

        assert str(exc_info.value) == f"DummyEntity with id={invalid_id} not found"

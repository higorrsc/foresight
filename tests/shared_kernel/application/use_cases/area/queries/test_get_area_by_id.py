from uuid import UUID

import pytest

from src.core.application.use_cases.queries import GetByIdRequestInputDTO
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.exceptions import AreaNotFoundError


class TestGetAreaByIdUseCase:
    """
    Test suite for the GetAreaByIdUseCase.
    """

    async def test_get_area_by_id_with_valid_id(
        self,
        admin_actor,
        area_in_memory_repo,
        get_area_by_id_use_case,
    ):
        """
        Test getting an area by a valid ID.
        """

        area = Area(description="Test Area", tenant_id=admin_actor.tenant_id)
        await area_in_memory_repo.save(area)

        retrieved_area = await get_area_by_id_use_case.execute(
            GetByIdRequestInputDTO(
                id=area.id,
                actor=admin_actor,
            )
        )

        assert retrieved_area.id == area.id
        assert retrieved_area.description == area.description

    async def test_get_area_by_id_with_non_existent_id(
        self,
        admin_actor,
        get_area_by_id_use_case,
    ):
        """
        Test getting an area by a non-existent ID.
        """

        non_existent_id: UUID = UUID("123e4567-e89b-12d3-a456-426614174000")

        with pytest.raises(AreaNotFoundError, match="Area with given ID not found."):
            await get_area_by_id_use_case.execute(
                GetByIdRequestInputDTO(
                    id=non_existent_id,
                    actor=admin_actor,
                )
            )

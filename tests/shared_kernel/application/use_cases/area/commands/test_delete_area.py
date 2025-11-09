from uuid import UUID

from src.shared_kernel.application._shared.use_cases.commands import (
    DeleteRequestInputDTO,
)
from src.shared_kernel.application.use_cases.area import AreaNotFoundError
from src.shared_kernel.application.use_cases.area.commands import DeleteAreaUseCase
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.infrastructure.repositories._shared import InMemoryRepository


class TestDeleteArea:
    """
    Test suite for the delete area use case.
    """

    def test_delete_area_with_valid_id(self, admin_actor):
        """
        Test deleting an area with a valid ID.
        """

        repository = InMemoryRepository[Area]()
        use_case = DeleteAreaUseCase(repository)

        area = Area(
            description="Area to be deleted",
            tenant_id=admin_actor.tenant_id,
        )
        repository.save(area)

        use_case.execute(
            DeleteRequestInputDTO(
                actor=admin_actor,
                id=area.id,
            )
        )
        deleted_area = repository.get_by_id(
            entity_id=area.id,
            tenant_id=admin_actor.tenant_id,
        )

        assert deleted_area is not None
        assert deleted_area.is_active is False
        assert deleted_area.deleted_at is not None

    def test_delete_non_existent_area(self, admin_actor):
        """
        Test deleting a non-existent area.
        """

        repository = InMemoryRepository[Area]()
        use_case = DeleteAreaUseCase(repository)

        non_existent_id: UUID = UUID("123e4567-e89b-12d3-a456-426614174000")

        try:
            use_case.execute(
                DeleteRequestInputDTO(
                    actor=admin_actor,
                    id=non_existent_id,
                )
            )
        except AreaNotFoundError as e:
            assert str(e) == "Area with given ID not found."

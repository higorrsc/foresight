from uuid import UUID

from src.core.application.use_cases.commands import DeleteRequestInputDTO
from src.shared_kernel.application.use_cases.area import AreaNotFoundError
from src.shared_kernel.domain.entities import Area


class TestDeleteArea:
    """
    Test suite for the delete area use case.
    """

    def test_delete_area_with_valid_id(
        self, admin_actor, area_in_memory_repo, delete_area_use_case
    ):
        """
        Test deleting an area with a valid ID.
        """

        area = Area(
            description="Area to be deleted",
            tenant_id=admin_actor.tenant_id,
        )
        area_in_memory_repo.save(area)

        delete_area_use_case.execute(
            DeleteRequestInputDTO(
                actor=admin_actor,
                id=area.id,
            )
        )
        deleted_area = area_in_memory_repo.get_by_id(
            entity_id=area.id,
            tenant_id=admin_actor.tenant_id,
        )

        assert deleted_area is not None
        assert deleted_area.is_active is False
        assert deleted_area.deleted_at is not None

    def test_delete_non_existent_area(self, admin_actor, delete_area_use_case):
        """
        Test deleting a non-existent area.
        """

        non_existent_id: UUID = UUID("123e4567-e89b-12d3-a456-426614174000")

        try:
            delete_area_use_case.execute(
                DeleteRequestInputDTO(
                    actor=admin_actor,
                    id=non_existent_id,
                )
            )
        except AreaNotFoundError as e:
            assert str(e) == "Area with given ID not found."

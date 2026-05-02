from datetime import datetime
from uuid import UUID

from src.core.application.use_cases.commands import RestoreRequestInputDTO
from src.shared_kernel.application.use_cases.area import AreaNotFoundError
from src.shared_kernel.domain.entities import Area


class TestRestoreArea:
    """
    Test suite for the restore area use case.
    """

    def test_restore_area_with_valid_id(
        self, admin_actor, area_in_memory_repo, restore_area_use_case
    ):
        """
        Test restoring an area with a valid ID.
        """

        area = Area(
            description="Area to be restored",
            tenant_id=admin_actor.tenant_id,
        )
        area.is_active = False
        area.deleted_at = datetime.now()
        area_in_memory_repo.save(area)

        restore_area_use_case.execute(
            RestoreRequestInputDTO(
                actor=admin_actor,
                id=area.id,
            )
        )
        restored_area = area_in_memory_repo.get_by_id(
            entity_id=area.id,
            tenant_id=admin_actor.tenant_id,
        )

        assert restored_area is not None
        assert restored_area.is_active is True
        assert restored_area.deleted_at is None

    def test_restore_non_existent_area(self, admin_actor, restore_area_use_case):
        """
        Test restoring a non-existent area.
        """

        non_existent_id: UUID = UUID("123e4567-e89b-12d3-a456-426614174000")

        try:
            restore_area_use_case.execute(
                RestoreRequestInputDTO(
                    actor=admin_actor,
                    id=non_existent_id,
                )
            )
        except AreaNotFoundError as e:
            assert str(e) == "Area with given ID not found."

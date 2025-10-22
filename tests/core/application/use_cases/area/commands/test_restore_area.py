from datetime import datetime
from uuid import UUID

from src.core.application._shared.use_cases.commands import RestoreRequestInputDTO
from src.core.application.use_cases.area import AreaNotFoundError
from src.core.application.use_cases.area.commands import RestoreAreaUseCase
from src.core.domain.entities import Area
from src.core.infrastructure.repositories._shared import InMemoryRepository


class TestRestoreArea:
    """
    Test suite for the restore area use case.
    """

    def test_restore_area_with_valid_id(self):
        """
        Test restoring an area with a valid ID.
        """

        repository = InMemoryRepository[Area]()
        use_case = RestoreAreaUseCase(repository)

        area = Area(description="Area to be restored")
        area.is_active = False
        area.deleted_at = datetime.now()
        repository.save(area)

        use_case.execute(RestoreRequestInputDTO(id=area.id))
        restored_area = repository.get_by_id(area.id)

        assert restored_area is not None
        assert restored_area.is_active is True
        assert restored_area.deleted_at is None

    def test_restore_non_existent_area(self):
        """
        Test restoring a non-existent area.
        """

        repository = InMemoryRepository[Area]()
        use_case = RestoreAreaUseCase(repository)

        non_existent_id: UUID = UUID("123e4567-e89b-12d3-a456-426614174000")

        try:
            use_case.execute(RestoreRequestInputDTO(id=non_existent_id))
        except AreaNotFoundError as e:
            assert str(e) == "Area with given ID not found."

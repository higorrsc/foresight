from core.application._shared.use_cases import InputDeleteRequestDTO
from core.application.use_cases.area import AreaNotFoundError, DeleteAreaUseCase
from core.domain.entities import Area
from core.tests.fakes.in_memory_repository import InMemoryRepository


class TestDeleteArea:
    """
    Test suite for the delete area use case.
    """

    def test_delete_area_with_valid_id(self):
        """
        Test deleting an area with a valid ID.
        """

        repository = InMemoryRepository[Area]()
        use_case = DeleteAreaUseCase(repository)

        area = Area(description="Area to be deleted")
        repository.save(area)

        use_case.execute(InputDeleteRequestDTO(id=area.id))

        assert repository.get_by_id(area.id) is None

    def test_delete_non_existent_area(self):
        """
        Test deleting a non-existent area.
        """

        repository = InMemoryRepository[Area]()
        use_case = DeleteAreaUseCase(repository)

        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"

        try:
            use_case.execute(InputDeleteRequestDTO(id=non_existent_id))
        except AreaNotFoundError as e:
            assert str(e) == "Area with given ID not found."

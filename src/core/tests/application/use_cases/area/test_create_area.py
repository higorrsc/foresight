from src.core.application.use_cases.area import (
    CreateAreaUseCase,
    InputCreateAreaDTO,
    OutputCreateAreaDTO,
)
from src.core.domain.entities import Area
from src.core.infrastructure.repositories._shared import InMemoryRepository


class TestCreateArea:
    """
    Test the CreateAreaUseCase.
    """

    def test_create_area_with_valid_data(self):
        """
        Test the creation of an area with valid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = CreateAreaUseCase(repository)
        output = use_case.execute(InputCreateAreaDTO("Test Area"))

        assert output.id is not None
        assert isinstance(output, OutputCreateAreaDTO)

    def test_create_area_with_invalid_data(self):
        """
        Test the creation of an area with invalid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = CreateAreaUseCase(repository)

        try:
            use_case.execute(InputCreateAreaDTO(""))
            assert False, "Expected ValueError for empty name"
        except ValueError as e:
            assert (
                str(e) == "Invalid input data: Description must be a non-empty string."
            )

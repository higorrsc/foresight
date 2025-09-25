from core.application.use_cases.area import (
    CreateArea,
    InputCreateAreaDTO,
    OutputCreateAreaDTO,
)
from core.domain.entities import Area
from core.tests.fakes import InMemoryRepository


class TestCreateArea:
    """
    Test the CreateArea use case.
    """

    def test_create_area_with_valid_data(self):
        """
        Test the creation of an area with valid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = CreateArea(repository)
        output = use_case.execute(InputCreateAreaDTO("Test Area"))

        assert output.id is not None
        assert isinstance(output, OutputCreateAreaDTO)

    def test_create_area_with_invalid_data(self):
        """
        Test the creation of an area with invalid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = CreateArea(repository)

        try:
            use_case.execute(InputCreateAreaDTO(""))
            assert False, "Expected ValueError for empty name"
        except ValueError as e:
            assert (
                str(e) == "Invalid input data: Description must be a non-empty string."
            )

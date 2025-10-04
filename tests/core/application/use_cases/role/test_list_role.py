import pytest

from src.core.application._shared.use_cases import ListRequestInputDTO
from src.core.application.use_cases.role import ListRoleUseCase
from src.core.domain.entities import Role
from src.core.infrastructure.repositories._shared import InMemoryRepository


class TestListRoleUseCase:
    """
    Test suite for the ListRoleUseCase.
    """

    @pytest.fixture
    def role_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return InMemoryRepository[Role]()

    def test_list_role(self, role_in_memory_repository):
        """
        Test list role.
        """

        repo = role_in_memory_repository

        new_role = Role(name="Test Role", description="Test Description")
        repo.save(new_role)

        use_case = ListRoleUseCase(repository=repo)

        output = use_case.execute(ListRequestInputDTO())

        assert output is not None
        assert len(output.data) == 1
        assert output.data[0].id == new_role.id

    def test_list_role_with_empty_list(self, role_in_memory_repository):
        """
        Test list role with empty list.
        """

        repo = role_in_memory_repository
        use_case = ListRoleUseCase(repository=repo)
        output = use_case.execute(ListRequestInputDTO())

        assert len(output.data) == 0

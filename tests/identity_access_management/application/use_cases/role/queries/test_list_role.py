import pytest

from src.identity_access_management.application.use_cases.role.queries import (
    ListRoleUseCase,
)
from src.identity_access_management.domain.entities import Role
from src.shared_kernel.application._shared.use_cases.queries import ListRequestInputDTO
from tests.fakes import RoleInMemoryRepository


class TestListRoleUseCase:
    """
    Test suite for the ListRoleUseCase.
    """

    @pytest.fixture
    def role_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return RoleInMemoryRepository()

    def test_list_role(self, role_in_memory_repository, admin_actor):
        """
        Test list role.
        """

        repo = role_in_memory_repository

        new_role = Role(
            name="Test Role",
            description="Test Description",
            tenant_id=admin_actor.tenant_id,
        )
        repo.save(new_role)

        use_case = ListRoleUseCase(repository=repo)

        output = use_case.execute(ListRequestInputDTO(actor=admin_actor))

        assert output is not None
        assert len(output.data) == 1
        assert output.data[0].id == new_role.id

    def test_list_role_with_empty_list(self, role_in_memory_repository, admin_actor):
        """
        Test list role with empty list.
        """

        repo = role_in_memory_repository
        use_case = ListRoleUseCase(repository=repo)
        output = use_case.execute(ListRequestInputDTO(actor=admin_actor))

        assert len(output.data) == 0

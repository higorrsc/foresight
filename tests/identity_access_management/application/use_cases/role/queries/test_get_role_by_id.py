import uuid

import pytest

from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.application.use_cases.role.queries import (
    GetRoleByIdUseCase,
)
from src.identity_access_management.domain.entities import Role
from src.shared_kernel.application._shared.use_cases.queries import (
    GetByIdRequestInputDTO,
)
from tests.fakes import RoleInMemoryRepository


class TestGetRoleByIdUseCase:
    """
    Test suite for the GetRoleByIdUseCase.
    """

    @pytest.fixture
    def role_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return RoleInMemoryRepository()

    def test_get_role_by_id(self, role_in_memory_repository, admin_actor):
        """
        Test get role by id.
        """

        new_role = Role(
            name="Test Role",
            description="Test Description",
            tenant_id=admin_actor.tenant_id,
        )

        repo = role_in_memory_repository
        repo.save(new_role)

        input_dto = GetByIdRequestInputDTO(id=new_role.id, actor=admin_actor)
        use_case = GetRoleByIdUseCase(repository=repo)
        output = use_case.execute(input_dto)

        assert output is not None
        assert output.id == new_role.id
        assert output.name == new_role.name
        assert output.description == new_role.description

    def test_get_role_by_id_with_invalid_id(
        self, role_in_memory_repository, admin_actor
    ):
        """
        Test get role by id with invalid id.
        """

        new_role = Role(
            name="Test Role",
            description="Test Description",
            tenant_id=admin_actor.tenant_id,
        )

        repo = role_in_memory_repository
        repo.save(new_role)

        input_dto = GetByIdRequestInputDTO(id=uuid.uuid4(), actor=admin_actor)
        use_case = GetRoleByIdUseCase(repository=repo)

        with pytest.raises(
            RoleNotFoundError,
            match="Role with given ID not found.",
        ):
            use_case.execute(input_dto)

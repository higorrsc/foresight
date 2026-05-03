import uuid

import pytest

from src.core.application.use_cases.queries import GetByIdRequestInputDTO
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.exceptions import RoleNotFoundError


class TestGetRoleByIdUseCase:
    """
    Test suite for the GetRoleByIdUseCase.
    """

    def test_get_role_by_id(
        self, role_in_memory_repo, get_role_by_id_use_case, admin_actor
    ):
        """
        Test get role by id.
        """

        new_role = Role(
            name="Test Role",
            description="Test Description",
            tenant_id=admin_actor.tenant_id,
        )

        role_in_memory_repo.save(new_role)

        input_dto = GetByIdRequestInputDTO(id=new_role.id, actor=admin_actor)
        output = get_role_by_id_use_case.execute(input_dto)

        assert output is not None
        assert output.id == new_role.id
        assert output.name == new_role.name
        assert output.description == new_role.description

    def test_get_role_by_id_with_invalid_id(self, get_role_by_id_use_case, admin_actor):
        """
        Test get role by id with invalid id.
        """

        input_dto = GetByIdRequestInputDTO(id=uuid.uuid4(), actor=admin_actor)

        with pytest.raises(
            RoleNotFoundError,
            match="Role with given ID not found.",
        ):
            get_role_by_id_use_case.execute(input_dto)

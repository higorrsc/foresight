from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.role import (
    InvalidRoleError,
    RoleNotFoundError,
)
from src.identity_access_management.application.use_cases.role.commands import (
    UpdateRoleInputDTO,
)
from src.identity_access_management.domain.entities import Role


class TestUpdateRoleUseCase:
    """
    Test suite for the UpdateRoleUseCase.
    """

    def test_update_role(
        self, role_in_memory_repo, update_role_use_case_iam, admin_actor
    ):
        """
        Test update role.
        """

        role = Role(
            name="Test",
            description="Test role",
            tenant_id=admin_actor.tenant_id,
        )
        role_in_memory_repo.save(role)

        input_dto = UpdateRoleInputDTO(
            id=role.id,
            name="Updated",
            description="Updated role",
            actor=admin_actor,
        )

        output = update_role_use_case_iam.execute(input_dto)

        assert output.name == "Updated"
        assert output.description == "Updated role"

    def test_update_role_with_invalid_name(
        self,
        role_in_memory_repo,
        update_role_use_case_iam,
        admin_actor,
    ):
        """
        Test update role with invalid name.
        """

        role = Role(
            name="Test",
            description="Test role",
            tenant_id=admin_actor.tenant_id,
        )
        role_in_memory_repo.save(role)

        input_dto = UpdateRoleInputDTO(
            id=role.id,
            name="a" * 101,
            description="Updated role",
            actor=admin_actor,
        )

        with pytest.raises(
            InvalidRoleError,
            match="Role name must be at most 100 characters long.",
        ):
            update_role_use_case_iam.execute(input_dto)

    def test_update_role_with_invalid_id(
        self, role_in_memory_repo, update_role_use_case_iam, admin_actor
    ):
        """ ""
        Test update role with invalid id.
        """

        role = Role(name="Test", description="Test role")
        role_in_memory_repo.save(role)

        invalid_id = uuid4()

        input_dto = UpdateRoleInputDTO(
            id=invalid_id,
            name="Updated",
            description="Updated role",
            actor=admin_actor,
        )

        with pytest.raises(
            RoleNotFoundError,
            match=f"Role with id {invalid_id} not found.",
        ):
            update_role_use_case_iam.execute(input_dto)

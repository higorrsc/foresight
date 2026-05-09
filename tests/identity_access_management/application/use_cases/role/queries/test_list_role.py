from src.core.application.use_cases.queries import ListRequestInputDTO
from src.identity_access_management.domain.entities import Role


class TestListRoleUseCase:
    """
    Test suite for the ListRoleUseCase.
    """

    async def test_list_role(
        self,
        role_in_memory_repo,
        list_role_use_case,
        admin_actor,
    ):
        """
        Test list role.
        """

        new_role = Role(
            name="Test Role",
            description="Test Description",
            tenant_id=admin_actor.tenant_id,
        )
        await role_in_memory_repo.save(new_role)

        output = await list_role_use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert output is not None
        assert len(output.data) == 1
        assert output.data[0].id == new_role.id

    async def test_list_role_with_empty_list(self, list_role_use_case, admin_actor):
        """
        Test list role with empty list.
        """

        output = await list_role_use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert len(output.data) == 0

from src.core.application.use_cases.queries import ListRequestInputDTO
from src.identity_access_management.domain.entities import Permission, User


class TestListPermissionsUseCase:
    """
    Test suite for the ListPermissionsUseCase.
    """

    def test_should_return_all_permissions(
        self,
        list_permissions_use_case,
        permission_in_memory_repo,
        admin_actor: User,
    ):
        """
        Test if the use case returns all permissions.
        """

        perms = [
            Permission(codename="user:read", description="Read users"),
            Permission(codename="user:write", description="Write users"),
        ]

        for p in perms:
            permission_in_memory_repo.save(p)

        input_dto = ListRequestInputDTO(actor=admin_actor)
        result = list_permissions_use_case.execute(input_dto)

        assert len(result.data) == 2
        assert isinstance(result.data[0], Permission)
        assert any(p.codename == "user:read" for p in result.data)
        assert any(p.codename == "user:write" for p in result.data)

    def test_should_return_empty_list_if_no_permissions(
        self,
        list_permissions_use_case,
        admin_actor: User,
    ):
        """
        Test if the use case returns an empty list if no permissions exist.
        """
        input_dto = ListRequestInputDTO(actor=admin_actor)
        result = list_permissions_use_case.execute(input_dto)

        assert result.data == []

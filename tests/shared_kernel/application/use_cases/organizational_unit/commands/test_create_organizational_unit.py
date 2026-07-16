from uuid import uuid4

import pytest

from src.shared_kernel.application.use_cases.organizational_unit.commands import (
    CreateOrganizationalUnitInputDTO,
    CreateOrganizationalUnitOutputDTO,
)
from src.shared_kernel.domain.exceptions import InvalidOrganizationalUnitError


class TestCreateOrganizationalUnitUseCase:
    """
    Test suite for the CreateOrganizationalUnitUseCase.
    """

    async def test_create_organizational_unit_success(
        self,
        create_organizational_unit_use_case,
        organizational_unit_in_memory_repo,
        admin_actor,
    ):
        """
        Test successful creation of an organizational unit.
        """
        input_dto = CreateOrganizationalUnitInputDTO(
            actor=admin_actor,
            description="Test Unit",
            code="TU001",
        )

        result = await create_organizational_unit_use_case.execute(input_dto)

        assert isinstance(result, CreateOrganizationalUnitOutputDTO)
        assert result.id is not None

        saved_entity = await organizational_unit_in_memory_repo.get_by_id(
            result.id, admin_actor.tenant_id
        )
        assert saved_entity is not None
        assert saved_entity.description == "Test Unit"
        assert saved_entity.code == "TU001"
        assert saved_entity.tenant_id == admin_actor.tenant_id
        assert saved_entity.created_by == admin_actor.id
        assert saved_entity.updated_by == admin_actor.id

    async def test_create_organizational_unit_with_parent(
        self,
        create_organizational_unit_use_case,
        organizational_unit_in_memory_repo,
        admin_actor,
    ):
        """
        Test successful creation of an organizational unit with a parent.
        """
        parent_id = uuid4()
        input_dto = CreateOrganizationalUnitInputDTO(
            actor=admin_actor,
            description="Child Unit",
            code="CU001",
            parent_id=parent_id,
        )

        result = await create_organizational_unit_use_case.execute(input_dto)

        assert result.id is not None
        saved_entity = await organizational_unit_in_memory_repo.get_by_id(
            result.id, admin_actor.tenant_id
        )
        assert saved_entity.parent_id == parent_id

    async def test_create_organizational_unit_invalid_data(
        self,
        create_organizational_unit_use_case,
        admin_actor,
    ):
        """
        Test creation failure when provided with invalid data.
        """

        input_dto = CreateOrganizationalUnitInputDTO(
            actor=admin_actor,
            description="",  # invalid
            code="TU001",
        )

        with pytest.raises(InvalidOrganizationalUnitError) as exc:
            await create_organizational_unit_use_case.execute(input_dto)

        assert "Invalid input data" in str(exc.value)

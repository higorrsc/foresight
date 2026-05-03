from uuid import uuid4

import pytest

from src.shared_kernel.application.use_cases.organizational_unit.commands import (
    UpdateOrganizationalUnitInputDTO,
    UpdateOrganizationalUnitOutputDTO,
)
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.exceptions import OrganizationalUnitNotFoundError


class TestUpdateOrganizationalUnitUseCase:
    """
    Test suite for the UpdateOrganizationalUnitUseCase.
    """

    def test_update_organizational_unit_success(
        self,
        update_organizational_unit_use_case,
        organizational_unit_in_memory_repo,
        admin_actor,
    ):
        """
        Test successful update of an organizational unit.
        """
        # Setup: Create an existing organizational unit
        entity_id = uuid4()
        original_entity = OrganizationalUnit(
            id=entity_id,
            tenant_id=admin_actor.tenant_id,
            description="Original Description",
            code="ORIG",
            created_by=admin_actor.id,
            updated_by=admin_actor.id,
        )
        organizational_unit_in_memory_repo.save(original_entity)

        input_dto = UpdateOrganizationalUnitInputDTO(
            actor=admin_actor,
            id=entity_id,
            description="Updated Description",
            code="UPDATED",
            parent_id=None,
        )

        result = update_organizational_unit_use_case.execute(input_dto)

        assert isinstance(result, UpdateOrganizationalUnitOutputDTO)
        assert result.id == entity_id
        assert result.description == "Updated Description"

        saved_entity = organizational_unit_in_memory_repo.get_by_id(
            entity_id, admin_actor.tenant_id
        )
        assert saved_entity is not None
        assert saved_entity.description == "Updated Description"
        assert saved_entity.code == "UPDATED"
        assert saved_entity.updated_by == admin_actor.id

    def test_update_organizational_unit_not_found(
        self, update_organizational_unit_use_case, admin_actor
    ):
        """
        Test that updating a non-existent organizational unit raises an error.
        """
        input_dto = UpdateOrganizationalUnitInputDTO(
            actor=admin_actor,
            id=uuid4(),
            description="Updated Description",
            code="UPDATED",
        )

        with pytest.raises(OrganizationalUnitNotFoundError):
            update_organizational_unit_use_case.execute(input_dto)

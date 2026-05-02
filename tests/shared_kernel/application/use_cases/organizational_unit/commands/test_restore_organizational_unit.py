from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_restore import (
    RestoreRequestInputDTO,
)
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.shared_kernel.application.use_cases.organizational_unit.exceptions import (
    OrganizationalUnitNotFoundError,
)
from src.shared_kernel.domain.entities import OrganizationalUnit


class TestRestoreOrganizationalUnitUseCase:
    """
    Test suite for the RestoreOrganizationalUnitUseCase.
    """

    def test_restore_organizational_unit_success(
        self,
        restore_organizational_unit_use_case,
        organizational_unit_in_memory_repo,
        admin_actor,
    ):
        """
        Test successful restoration of a soft-deleted organizational unit.
        """
        admin_actor.permissions.add(AppPermission.ORGANIZATIONAL_UNIT_DELETE)

        entity_id = uuid4()
        entity = OrganizationalUnit(
            id=entity_id,
            tenant_id=admin_actor.tenant_id,
            description="Test Unit",
            code="TU001",
            created_by=admin_actor.id,
            updated_by=admin_actor.id,
        )
        entity.soft_delete()
        organizational_unit_in_memory_repo.save(entity)

        assert entity.deleted_at is not None

        input_dto = RestoreRequestInputDTO(
            actor=admin_actor,
            id=entity_id,
        )

        restore_organizational_unit_use_case.execute(input_dto)

        saved_entity = organizational_unit_in_memory_repo.get_by_id(
            entity_id, admin_actor.tenant_id
        )
        assert saved_entity is not None
        assert saved_entity.deleted_at is None
        assert saved_entity.updated_by == admin_actor.id

    def test_restore_organizational_unit_insufficient_permission(
        self,
        restore_organizational_unit_use_case,
        organizational_unit_in_memory_repo,
        admin_actor,
    ):
        """
        Test that restoration fails when the actor has insufficient permissions.
        """
        # Create an actor without the required permission
        from copy import deepcopy

        actor_no_perm = deepcopy(admin_actor)
        if AppPermission.ORGANIZATIONAL_UNIT_DELETE in actor_no_perm.permissions:
            actor_no_perm.permissions.remove(AppPermission.ORGANIZATIONAL_UNIT_DELETE)

        input_dto = RestoreRequestInputDTO(
            actor=actor_no_perm,
            id=uuid4(),
        )

        with pytest.raises(InsufficientPermissionError):
            restore_organizational_unit_use_case.execute(input_dto)

    def test_restore_organizational_unit_not_found(
        self, restore_organizational_unit_use_case, admin_actor
    ):
        """
        Test that restoration fails when the organizational unit is not found.
        """
        admin_actor.permissions.add(AppPermission.ORGANIZATIONAL_UNIT_DELETE)

        input_dto = RestoreRequestInputDTO(
            actor=admin_actor,
            id=uuid4(),
        )

        with pytest.raises(OrganizationalUnitNotFoundError):
            restore_organizational_unit_use_case.execute(input_dto)

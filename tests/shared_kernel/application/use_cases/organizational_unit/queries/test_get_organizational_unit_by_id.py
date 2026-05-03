from uuid import uuid4

import pytest

from src.core.application.use_cases.queries.generic_get_by_id import (
    GetByIdRequestInputDTO,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.exceptions import OrganizationalUnitNotFoundError


class TestGetOrganizationalUnitByIdUseCase:
    """
    Test suite for the GetOrganizationalUnitByIdUseCase.
    """

    def test_get_organizational_unit_by_id_success(
        self,
        get_organizational_unit_by_id_use_case,
        organizational_unit_in_memory_repo,
        admin_actor,
    ):
        """
        Test successful retrieval of an organizational unit by its ID.
        """
        admin_actor.permissions.add(AppPermission.ORGANIZATIONAL_UNIT_READ)

        entity_id = uuid4()
        entity = OrganizationalUnit(
            id=entity_id,
            tenant_id=admin_actor.tenant_id,
            description="Test Unit",
            code="TU001",
            created_by=admin_actor.id,
            updated_by=admin_actor.id,
        )
        organizational_unit_in_memory_repo.save(entity)

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=entity_id,
        )

        result = get_organizational_unit_by_id_use_case.execute(input_dto)

        assert result == entity
        assert result.id == entity_id

    def test_get_organizational_unit_by_id_insufficient_permission(
        self, get_organizational_unit_by_id_use_case, admin_actor
    ):
        """
        Test that retrieval fails when the actor has insufficient permissions.
        """
        # Create an actor without the required permission
        from copy import deepcopy

        actor_no_perm = deepcopy(admin_actor)
        if AppPermission.ORGANIZATIONAL_UNIT_READ in actor_no_perm.permissions:
            actor_no_perm.permissions.remove(AppPermission.ORGANIZATIONAL_UNIT_READ)

        input_dto = GetByIdRequestInputDTO(
            actor=actor_no_perm,
            id=uuid4(),
        )

        with pytest.raises(InsufficientPermissionError):
            get_organizational_unit_by_id_use_case.execute(input_dto)

    def test_get_organizational_unit_by_id_not_found(
        self, get_organizational_unit_by_id_use_case, admin_actor
    ):
        """
        Test that retrieval fails when the organizational unit is not found.
        """
        admin_actor.permissions.add(AppPermission.ORGANIZATIONAL_UNIT_READ)

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=uuid4(),
        )

        with pytest.raises(OrganizationalUnitNotFoundError):
            get_organizational_unit_by_id_use_case.execute(input_dto)

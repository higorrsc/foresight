from typing import Any, Optional
from uuid import uuid4

import pytest

from src.core.domain.exceptions import EntityValidationError
from src.tenant_management.domain.entities.tenant import Tenant
from src.tenant_management.domain.value_objects import TenantStatus


class TestTenant:
    """
    Test suite for the Tenant entity.
    """

    def test_create_tenant_with_valid_data(self) -> None:
        """
        Should create a Tenant instance successfully when provided with valid data.
        """
        tenant_id = uuid4()
        name = "Acme Inc."
        plan_id = uuid4()

        tenant = Tenant(
            id=tenant_id,
            name=name,
            plan_id=plan_id,
            status=TenantStatus.ACTIVE,
        )
        tenant.validate()

        assert tenant.id == tenant_id
        assert tenant.name == name
        assert tenant.plan_id == plan_id
        assert tenant.status == TenantStatus.ACTIVE

    def test_create_tenant_defaults_status_to_trial(self) -> None:
        """
        Should default the status to TRIAL if not provided.
        """

        tenant = Tenant(name="Trial Tenant", plan_id=uuid4())

        assert tenant.status == TenantStatus.TRIAL

    @pytest.mark.parametrize(
        "name, expected_error",
        [
            (None, "Tenant name is required."),
            ("", "Tenant name is required."),
            ("   ", "Tenant name is required."),
            ("a" * 101, "Tenant must be at most 100 characters long."),
        ],
    )
    def test_create_tenant_with_invalid_name_raises_error(
        self,
        name: Optional[str] | None,
        expected_error: str,
    ) -> None:
        """
        Should raise EntityValidationError for invalid names.
        """

        with pytest.raises(
            EntityValidationError,
            match=expected_error,
        ):
            Tenant(name=name, plan_id=uuid4())  # type: ignore

    @pytest.mark.parametrize(
        "plan_id, expected_error",
        [
            (None, "Tenant plan_id must be a valid UUID."),
            ("not-a-uuid", "Tenant plan_id must be a valid UUID."),
        ],
    )
    def test_create_tenant_with_invalid_plan_id_raises_error(
        self, plan_id: Any, expected_error: str
    ) -> None:
        """
        Should raise EntityValidationError for invalid plan_id.
        """

        with pytest.raises(EntityValidationError, match=expected_error):
            Tenant(name="Valid Name", plan_id=plan_id)

    def test_create_tenant_with_invalid_status_raises_error(self) -> None:
        """
        Should raise EntityValidationError for an invalid status type.
        """

        with pytest.raises(
            EntityValidationError,
            match="Tenant status must be a valid TenantStatus.",
        ):
            Tenant(name="Valid Name", plan_id=uuid4(), status="invalid_status")  # type: ignore

    def test_tenant_string_representation(self) -> None:
        """
        Should return the correct string representation for the Tenant entity.
        """
        tenant_id = uuid4()
        tenant = Tenant(id=tenant_id, name="Test Tenant", plan_id=uuid4())

        assert str(tenant) == f"Tenant(id={tenant.id}, name='{tenant.name}')"

    def test_tenant_detailed_representation(self) -> None:
        """
        Should return the correct detailed string representation for the Tenant entity.
        """

        tenant_id = uuid4()
        tenant = Tenant(id=tenant_id, name="Test Tenant", plan_id=uuid4())

        assert repr(tenant) == f"<Tenant {tenant.name} ({tenant.id})>"

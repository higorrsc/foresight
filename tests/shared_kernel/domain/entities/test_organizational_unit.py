import uuid

import pytest

from src.shared_kernel.domain._shared import EntityValidationError
from src.shared_kernel.domain.entities import OrganizationalUnit


class TestOrganizationalUnitEntity:
    """
    Test suite for entity of OrganizationalUnit entities.
    """

    def test_organizational_units_with_same_id_are_equal(self):
        """
        Test that two OrganizationalUnit entities with the same ID are considered equal.
        """
        org_unit_id = uuid.uuid4()
        org_unit1 = OrganizationalUnit(
            code="OU1",
            description="Org Unit 1",
            id=org_unit_id,
        )
        org_unit2 = OrganizationalUnit(
            code="OU2",
            description="Org Unit 2",
            id=org_unit_id,
        )

        assert org_unit1 == org_unit2

    def test_organizational_units_with_different_ids_are_not_equal(self):
        """
        Test that two OrganizationalUnit entities with different IDs are not considered equal.
        """

        org_unit1 = OrganizationalUnit(
            code="OU1",
            description="Org Unit 1",
        )
        org_unit2 = OrganizationalUnit(
            code="OU2",
            description="Org Unit 2",
        )

        assert org_unit1 != org_unit2

    def test_organizational_unit_not_equal_to_different_type(self):
        """
        Test that an OrganizationalUnit entity is not equal to an object of a different type.
        """

        org_unit = OrganizationalUnit(
            code="OU1",
            description="Org Unit 1",
        )
        non_org_unit_object = "Not an OrganizationalUnit"

        assert org_unit != non_org_unit_object

    def test_organizational_unit_str(self):
        """
        Test the __str__ method of the OrganizationalUnit entity.
        """

        org_unit_id = uuid.uuid4()
        org_unit = OrganizationalUnit(
            id=org_unit_id,
            code="OU1",
            description="Org Unit 1",
        )

        assert str(org_unit) == f"OrganizationalUnit(id={org_unit_id}, code='OU1')"

    def test_organizational_unit_repr(self):
        """
        Test the __repr__ method of the OrganizationalUnit entity.
        """
        org_unit_id = uuid.uuid4()
        org_unit = OrganizationalUnit(
            id=org_unit_id,
            code="OU1",
            description="Org Unit 1",
        )

        assert repr(org_unit) == f"<OrganizationalUnit OU1 ({org_unit_id})>"

    def test_organizational_unit_creation(self):
        """
        Test that an OrganizationalUnit entity is created successfully with valid data.
        """

        org_unit_id = uuid.uuid4()
        org_unit = OrganizationalUnit(
            id=org_unit_id,
            code="OU1",
            description="Org Unit 1",
        )

        assert org_unit.id == org_unit_id
        assert org_unit.code == "OU1"
        assert org_unit.description == "Org Unit 1"
        assert org_unit.parent_id is None

    def test_organization_unit_description_required(self):
        """
        Test that creating an OrganizationalUnit entity without a description
        raises a EntityValidationError.
        """

        with pytest.raises(EntityValidationError):
            OrganizationalUnit(code="OU1", description="")

    def test_organizational_unit_creation_with_parent_id(self):
        """
        Test that creating an OrganizationUnit entity with parent_id works as expected.
        """

        parent_org_unit = OrganizationalUnit(
            code="OU1",
            description="Parent Org Unit",
        )

        child_org_unit = OrganizationalUnit(
            code="OU2",
            description="Child Org Unit",
            parent_id=parent_org_unit.id,
        )

        assert child_org_unit.parent_id is not None
        assert child_org_unit.parent_id == parent_org_unit.id

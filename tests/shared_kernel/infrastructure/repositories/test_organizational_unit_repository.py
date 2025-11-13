from uuid import uuid4

import pytest

from src.shared_kernel.infrastructure.models import OrganizationalUnitModel
from src.shared_kernel.infrastructure.repositories import OrganizationalUnitRepository


@pytest.fixture
def repository(db_session_for_test):
    """
    Fixture to provide a repository instance for testing.
    """

    return OrganizationalUnitRepository(db_session_for_test)


class TestOrganizationalUnitRepository:
    """
    Test suite for OrganizationalUnitRepository.
    """

    def test_get_by_parent_id(self, repository, db_session_for_test, default_tenant_id):
        """
        Test retrieving organizational units by parent_id.
        """

        # 1. Setup: Create parent and child units
        parent_id = uuid4()
        parent_unit = OrganizationalUnitModel(
            id=parent_id,
            code="1",
            description="Parent Unit",
            parent_id=None,
            tenant_id=default_tenant_id,
        )

        # Children ordered by code to test sorting
        child_unit_2 = OrganizationalUnitModel(
            code="1.2",
            description="Child Unit 2",
            parent_id=parent_id,
            tenant_id=default_tenant_id,
        )
        child_unit_1 = OrganizationalUnitModel(
            code="1.1",
            description="Child Unit 1",
            parent_id=parent_id,
            tenant_id=default_tenant_id,
        )

        # Another top-level unit
        other_parent_unit = OrganizationalUnitModel(
            code="2",
            description="Other Parent",
            parent_id=None,
            tenant_id=default_tenant_id,
        )

        db_session_for_test.add_all(
            [
                parent_unit,
                child_unit_1,
                child_unit_2,
                other_parent_unit,
            ]
        )
        db_session_for_test.flush()

        # 2. Test fetching children of a specific parent
        children = repository.get_by_parent_id(
            parent_id,
            tenant_id=default_tenant_id,
        )

        assert len(children) == 2
        assert children[0].code == "1.1"
        assert children[1].code == "1.2"
        assert children[0].description == "Child Unit 1"
        assert children[1].description == "Child Unit 2"

        # 3. Test fetching top-level units (parent_id is None)
        top_level_units = repository.get_by_parent_id(None, default_tenant_id)

        assert len(top_level_units) == 2
        assert top_level_units[0].code == "1"
        assert top_level_units[1].code == "2"

        # 4. Test fetching for a parent with no children
        no_children = repository.get_by_parent_id(
            other_parent_unit.id,
            tenant_id=default_tenant_id,
        )
        assert len(no_children) == 0

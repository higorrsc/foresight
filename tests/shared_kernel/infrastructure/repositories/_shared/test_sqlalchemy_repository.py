import pytest

from src.shared_kernel.infrastructure.mappers import AreaMapper
from src.shared_kernel.infrastructure.models import AreaModel
from src.shared_kernel.infrastructure.repositories._shared import SQLAlchemyRepository


@pytest.fixture
def repository(db_session_for_test):
    """
    Fixture to provide a repository instance for testing.
    """

    return SQLAlchemyRepository(
        db_session_for_test,
        AreaModel,
        AreaMapper,
    )


class TestSQLAlchemyRepository:
    """
    Test suite for SQLAlchemyRepository.
    """

    def test_save_and_get_by_id(self, repository, default_tenant_id):
        """
        Test saving an entity and retrieving it by ID.
        """

        area = AreaModel(
            description="Test Area",
            tenant_id=default_tenant_id,
        )
        saved_area = repository.save(area)

        assert saved_area.id is not None

        fetched_area = repository.get_by_id(
            entity_id=saved_area.id,
            tenant_id=default_tenant_id,
        )
        assert fetched_area is not None
        assert fetched_area.description == "Test Area"

    def test_list(self, repository, default_tenant_id):
        """
        Test listing all entities.
        """

        area1 = AreaModel(
            description="Area 1",
            tenant_id=default_tenant_id,
        )
        area2 = AreaModel(
            description="Area 2",
            tenant_id=default_tenant_id,
        )
        repository.save(area1)
        repository.save(area2)

        areas = repository.list(tenant_id=default_tenant_id)
        assert len(areas) == 2
        assert areas[0].description == "Area 1"
        assert areas[1].description == "Area 2"

    def test_update(self, repository, default_tenant_id):
        """
        Test updating an entity.
        """

        area = AreaModel(
            description="Old Description",
            tenant_id=default_tenant_id,
        )
        saved_area = repository.save(area)

        saved_area.description = "New Description"
        updated_area = repository.update(saved_area)

        assert updated_area.description == "New Description"

        fetched_area = repository.get_by_id(
            entity_id=saved_area.id,
            tenant_id=default_tenant_id,
        )
        assert fetched_area.description == "New Description"

    def test_delete(self, repository, default_tenant_id):
        """
        Test deleting an entity.
        """

        area = AreaModel(
            description="To be deleted",
            tenant_id=default_tenant_id,
        )
        saved_area = repository.save(area)

        repository.delete(
            entity_id=saved_area.id,
            tenant_id=default_tenant_id,
        )

        fetched_area = repository.get_by_id(
            saved_area.id,
            tenant_id=default_tenant_id,
        )
        assert fetched_area is None

from src.shared_kernel.infrastructure.models import AreaModel


class TestSQLAlchemyRepository:
    """
    Test suite for SQLAlchemyRepository.
    """

    async def test_save_and_get_by_id(
        self, sqlalchemy_area_repository, default_tenant_id
    ):
        """
        Test saving an entity and retrieving it by ID.
        """

        area = AreaModel(
            description="Test Area",
            tenant_id=default_tenant_id,
        )
        saved_area = await sqlalchemy_area_repository.save(area)

        assert saved_area.id is not None

        fetched_area = await sqlalchemy_area_repository.get_by_id(
            entity_id=saved_area.id,
            tenant_id=default_tenant_id,
        )
        assert fetched_area is not None
        assert fetched_area.description == "Test Area"

    async def test_get_all(self, sqlalchemy_area_repository, default_tenant_id):
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
        await sqlalchemy_area_repository.save(area1)
        await sqlalchemy_area_repository.save(area2)

        areas = await sqlalchemy_area_repository.get_all(tenant_id=default_tenant_id)
        assert len(areas) == 2
        assert areas[0].description == "Area 1"
        assert areas[1].description == "Area 2"

    async def test_update(self, sqlalchemy_area_repository, default_tenant_id):
        """
        Test updating an entity.
        """

        area = AreaModel(
            description="Old Description",
            tenant_id=default_tenant_id,
        )
        saved_area = await sqlalchemy_area_repository.save(area)

        saved_area.description = "New Description"
        updated_area = await sqlalchemy_area_repository.update(saved_area)

        assert updated_area.description == "New Description"

        fetched_area = await sqlalchemy_area_repository.get_by_id(
            entity_id=saved_area.id,
            tenant_id=default_tenant_id,
        )
        assert fetched_area.description == "New Description"

    async def test_delete(self, sqlalchemy_area_repository, default_tenant_id):
        """
        Test deleting an entity.
        """

        area = AreaModel(
            description="To be deleted",
            tenant_id=default_tenant_id,
        )
        saved_area = await sqlalchemy_area_repository.save(area)

        await sqlalchemy_area_repository.delete(
            entity_id=saved_area.id,
            tenant_id=default_tenant_id,
        )

        fetched_area = await sqlalchemy_area_repository.get_by_id(
            saved_area.id,
            tenant_id=default_tenant_id,
        )
        assert fetched_area is None

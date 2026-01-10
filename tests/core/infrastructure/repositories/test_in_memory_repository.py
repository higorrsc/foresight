from uuid import UUID

from src.core.infrastructure.repository import InMemoryRepository
from tests.fakes.dummy_entity import DummyEntity


class TestInMemoryRepository:
    """
    Test cases for the InMemoryRepository class.
    """

    def test_save_entity(self, default_tenant_id):
        """
        Test saving an entity to the repository.
        """

        repository: InMemoryRepository = InMemoryRepository()
        entity = DummyEntity(
            name="Test Entity",
            tenant_id=default_tenant_id,
        )
        saved_entity = repository.save(entity)

        assert saved_entity == entity

        found_entity = repository.get_by_id(
            entity_id=entity.id,
            tenant_id=default_tenant_id,
        )
        assert found_entity == entity

    def test_get_by_id_found(self, default_tenant_id):
        """
        Test retrieving an entity by ID when it exists.
        """

        entity = DummyEntity(
            name="Test Entity",
            tenant_id=default_tenant_id,
        )
        repository = InMemoryRepository(entities=[entity])
        found_entity = repository.get_by_id(
            entity_id=entity.id,
            tenant_id=default_tenant_id,
        )

        assert found_entity == entity

    def test_get_by_id_not_found(self, default_tenant_id):
        """
        Test retrieving an entity by ID when it does not exist.
        """

        repository: InMemoryRepository = InMemoryRepository()
        found_entity = repository.get_by_id(
            entity_id=UUID("12345678-1234-5678-1234-567812345678"),
            tenant_id=default_tenant_id,
        )

        assert found_entity is None

    def test_list_entities(self, default_tenant_id):
        """
        Test listing all entities in the repository.
        """

        entity1 = DummyEntity(
            name="Entity 1",
            tenant_id=default_tenant_id,
        )
        entity2 = DummyEntity(
            name="Entity 2",
            tenant_id=default_tenant_id,
        )
        repository = InMemoryRepository(entities=[entity1, entity2])
        entities = repository.list(tenant_id=default_tenant_id)

        assert entities == [entity1, entity2]

    def test_update_entity(self, default_tenant_id):
        """
        Test updating an existing entity in the repository.
        """

        entity = DummyEntity(
            name="Old Name",
            tenant_id=default_tenant_id,
        )
        repository: InMemoryRepository = InMemoryRepository(entities=[entity])

        updated_entity = DummyEntity(
            id=entity.id,
            name="New Name",
            tenant_id=default_tenant_id,
        )
        repository.update(updated_entity)

        found_entity = repository.get_by_id(
            entity_id=entity.id,
            tenant_id=default_tenant_id,
        )
        assert found_entity.name == "New Name"  # type: ignore

    def test_delete_entity(self, default_tenant_id):
        """
        Test deleting an entity from the repository.
        """

        entity = DummyEntity(
            name="To Be Deleted",
            tenant_id=default_tenant_id,
        )
        repository: InMemoryRepository = InMemoryRepository(entities=[entity])

        repository.delete(
            entity_id=entity.id,
            tenant_id=default_tenant_id,
        )
        found_entity = repository.get_by_id(
            entity.id,
            tenant_id=default_tenant_id,
        )

        assert found_entity is None

from uuid import UUID

from core.tests.fakes import DummyEntity, InMemoryRepository


class TestAbstractRepository:
    """
    Test cases for the AbstractRepository class.
    """

    def test_save_entity(self):
        """
        Test saving an entity to the repository.
        """

        repository = InMemoryRepository()
        entity = DummyEntity(name="Test Entity")
        saved_entity = repository.save(entity)

        assert saved_entity == entity
        assert repository.get_by_id(entity.id) == entity

    def test_get_by_id_found(self):
        """
        Test retrieving an entity by ID when it exists.
        """

        entity = DummyEntity(name="Test Entity")
        repository = InMemoryRepository(entities=[entity])
        found_entity = repository.get_by_id(entity.id)

        assert found_entity == entity

    def test_get_by_id_not_found(self):
        """
        Test retrieving an entity by ID when it does not exist.
        """

        repository = InMemoryRepository()
        found_entity = repository.get_by_id(
            UUID("12345678-1234-5678-1234-567812345678")
        )

        assert found_entity is None

    def test_list_entities(self):
        """
        Test listing all entities in the repository.
        """

        entity1 = DummyEntity(name="Entity 1")
        entity2 = DummyEntity(name="Entity 2")
        repository = InMemoryRepository(entities=[entity1, entity2])
        entities = repository.list()

        assert entities == [entity1, entity2]

    def test_update_entity(self):
        """
        Test updating an existing entity in the repository.
        """

        entity = DummyEntity(name="Old Name")
        repository = InMemoryRepository(entities=[entity])

        updated_entity = DummyEntity(id=entity.id, name="New Name")
        repository.update(updated_entity)

        found_entity = repository.get_by_id(entity.id)
        assert found_entity.name == "New Name"  # type: ignore

    def test_delete_entity(self):
        """
        Test deleting an entity from the repository.
        """

        entity = DummyEntity(name="To Be Deleted")
        repository = InMemoryRepository(entities=[entity])

        repository.delete(entity.id)
        found_entity = repository.get_by_id(entity.id)

        assert found_entity is None

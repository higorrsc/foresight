from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from src.core.domain._shared import AbstractRepository
from src.core.domain._shared.entity import AbstractEntity


@dataclass(kw_only=True, eq=False)
class DummyEntity(AbstractEntity):
    """
    A dummy entity for testing purposes.
    """

    name: str

    def _validate(self) -> None:
        if not self.name:
            self.notification.add_error("Name cannot be empty")
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)


class ConcreteRepository(AbstractRepository[DummyEntity]):
    """
    A concrete implementation of AbstractRepository for testing.
    """

    def __init__(self, entities: Optional[List[DummyEntity]] = None):
        """
        Initialize the repository with an optional list of entities.
        """

        self.entities = entities or []

    def save(self, entity: DummyEntity) -> Optional[DummyEntity]:
        """
        Save an entity to the repository.

        :param entity: The entity to be saved.
        :return: None
        """

        self.entities.append(entity)
        return entity

    def get_by_id(self, entity_id: UUID) -> Optional[DummyEntity]:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :return: The entity if found, otherwise None.
        """

        for entity in self.entities:
            if entity.id == entity_id:
                return entity

        return None

    def list(self) -> List[DummyEntity]:
        """
        List all entities in the repository.

        :return: A list of all entities.
        """

        return self.entities

    def update(self, entity: DummyEntity) -> Optional[DummyEntity]:
        """
        Update an existing entity in the repository.

        :param entity: The entity to be updated.
        :return: None
        """

        old_entity = self.get_by_id(entity.id)

        if old_entity:
            self.entities.remove(old_entity)
            self.entities.append(entity)

        return entity

    def delete(self, entity_id: UUID) -> None:
        """
        Delete an entity from the repository.

        :param entity_id: The ID of the entity to be deleted.
        """

        old_entity = self.get_by_id(entity_id)

        if old_entity:
            self.entities.remove(old_entity)


class TestAbstractRepository:
    """
    Test cases for the AbstractRepository class.
    """

    def test_save_entity(self):
        """
        Test saving an entity to the repository.
        """

        repository = ConcreteRepository()
        entity = DummyEntity(name="Test Entity")
        saved_entity = repository.save(entity)

        assert saved_entity == entity
        assert repository.get_by_id(entity.id) == entity

    def test_get_by_id_found(self):
        """
        Test retrieving an entity by ID when it exists.
        """

        entity = DummyEntity(name="Test Entity")
        repository = ConcreteRepository(entities=[entity])
        found_entity = repository.get_by_id(entity.id)

        assert found_entity == entity

    def test_get_by_id_not_found(self):
        """
        Test retrieving an entity by ID when it does not exist.
        """

        repository = ConcreteRepository()
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
        repository = ConcreteRepository(entities=[entity1, entity2])
        entities = repository.list()

        assert entities == [entity1, entity2]

    def test_update_entity(self):
        """
        Test updating an existing entity in the repository.
        """

        entity = DummyEntity(name="Old Name")
        repository = ConcreteRepository(entities=[entity])

        updated_entity = DummyEntity(id=entity.id, name="New Name")
        repository.update(updated_entity)

        found_entity = repository.get_by_id(entity.id)
        assert found_entity.name == "New Name"  # type: ignore

    def test_delete_entity(self):
        """
        Test deleting an entity from the repository.
        """

        entity = DummyEntity(name="To Be Deleted")
        repository = ConcreteRepository(entities=[entity])

        repository.delete(entity.id)
        found_entity = repository.get_by_id(entity.id)

        assert found_entity is None

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.infrastructure.mappers import AreaMapper
from src.core.infrastructure.models import AreaModel
from src.core.infrastructure.repositories._shared import SQLAlchemyRepository

Base = declarative_base()


@pytest.fixture
def session():
    """
    Fixture to create a new database session for each test.
    """

    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    AreaModel.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def repository(session):
    """
    Fixture to provide a repository instance for testing.
    """

    return SQLAlchemyRepository(
        session,
        AreaModel,
        AreaMapper,
    )


class TestSQLAlchemyRepository:
    """
    Test suite for SQLAlchemyRepository.
    """

    def test_save_and_get_by_id(self, repository):
        """
        Test saving an entity and retrieving it by ID.
        """

        area = AreaModel(description="Test Area")
        saved_area = repository.save(area)

        assert saved_area.id is not None

        fetched_area = repository.get_by_id(saved_area.id)
        assert fetched_area is not None
        assert fetched_area.description == "Test Area"

    def test_list(self, repository):
        """
        Test listing all entities.
        """

        area1 = AreaModel(description="Area 1")
        area2 = AreaModel(description="Area 2")
        repository.save(area1)
        repository.save(area2)

        areas = repository.list()
        assert len(areas) == 2
        assert areas[0].description == "Area 1"
        assert areas[1].description == "Area 2"

    def test_update(self, repository):
        """
        Test updating an entity.
        """

        area = AreaModel(description="Old Description")
        saved_area = repository.save(area)

        saved_area.description = "New Description"
        updated_area = repository.update(saved_area)

        assert updated_area.description == "New Description"

        fetched_area = repository.get_by_id(saved_area.id)
        assert fetched_area.description == "New Description"

    def test_delete(self, repository):
        """
        Test deleting an entity.
        """

        area = AreaModel(description="To be deleted")
        saved_area = repository.save(area)

        repository.delete(saved_area.id)

        fetched_area = repository.get_by_id(saved_area.id)
        assert fetched_area is None

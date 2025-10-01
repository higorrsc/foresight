import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.domain.entities.role import Role
from src.core.infrastructure.config.database import Base
from src.core.infrastructure.repositories import RoleRepository


@pytest.fixture(scope="function")
def session():
    """
    Create a new database session for each test.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db_session = SessionLocal()
    yield db_session

    db_session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def role_repository(session):
    """
    Create a RoleRepository instance for testing.
    """
    return RoleRepository(session)


class TestRoleRepository:
    """
    Test suite for RoleRepository.
    """

    def test_save_and_get_by_id(self, role_repository):
        """
        Test saving a role and retrieving it by ID.
        """

        role = Role(name="admin", description="Administrator role")
        saved_role = role_repository.save(role)

        assert saved_role is not None
        assert saved_role.id == role.id

        found_role = role_repository.get_by_id(role.id)
        assert found_role is not None
        assert found_role.name == "admin"

    def test_get_by_name_found(self, role_repository):
        """
        Test retrieving a role by name when it exists.
        """

        role = Role(name="viewer", description="Viewer role")
        role_repository.save(role)

        found_role = role_repository.get_by_name("viewer")

        assert found_role is not None
        assert found_role.id == role.id
        assert found_role.name == "viewer"

    def test_get_by_name_not_found(self, role_repository):
        """
        Test retrieving a role by name when it does not exist.
        """

        found_role = role_repository.get_by_name("non_existent_role")
        assert found_role is None

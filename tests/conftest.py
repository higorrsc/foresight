import os
from collections.abc import Generator
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock  # noqa: E402
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, Pool, StaticPool

from src.api.auth.local_provider import LocalAuthenticationProvider
from src.api.dependencies import get_db_session
from src.api.main import app
from src.core.application.use_cases.commands import GenericDeleteUseCase
from src.core.application.use_cases.queries import (
    GenericGetByIdUseCase,
    GenericListUseCase,
)
from src.core.domain import EntityNotFoundError
from src.core.infrastructure.config import Base
from src.core.infrastructure.repository import InMemoryRepository, SQLAlchemyRepository
from src.finance.domain.value_objects import CurrencyCode, Money
from src.identity_access_management.application.use_cases.permission.queries import (
    ListPermissionsUseCase,
)
from src.identity_access_management.application.use_cases.role.commands import (
    CreateRoleUseCase,
    SetRolePermissionsUseCase,
)
from src.identity_access_management.application.use_cases.role.commands import (
    DeleteRoleUseCase as DeleteRoleUseCase_IAM,
)
from src.identity_access_management.application.use_cases.role.commands import (
    RestoreRoleUseCase as RestoreRoleUseCase_IAM,
)
from src.identity_access_management.application.use_cases.role.commands import (
    UpdateRoleUseCase as UpdateRoleUseCase_IAM,
)
from src.identity_access_management.application.use_cases.role.queries import (
    GetRoleByIdUseCase,
    ListRoleUseCase,
)
from src.identity_access_management.application.use_cases.user.commands import (
    AuthenticateUserUseCase,
    ChangePasswordUseCase,
    CreateUserUseCase,
    DeleteUserUseCase,
    OnboardingUseCase,
    RestoreUserUseCase,
    SetUserPermissionsUseCase,
    SetUserRolesUseCase,
    UpdateUserProfileUseCase,
)
from src.identity_access_management.application.use_cases.user.queries import (
    GetUserByIdUseCase,
    ListUserUseCase,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import Role as RoleEntity
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.entities import User as UserEntity
from src.identity_access_management.infrastructure.mappers import RoleMapper, UserMapper
from src.identity_access_management.infrastructure.models import RoleModel, UserModel
from src.identity_access_management.infrastructure.repositories import (
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.planning.application.use_cases.scenario.commands import (
    CreateScenarioUseCase,
    DeleteScenarioUseCase,
    LockScenarioUseCase,
    RestoreScenarioUseCase,
    UnlockScenarioUseCase,
    UpdateScenarioUseCase,
)
from src.planning.application.use_cases.scenario.queries import (
    GetScenarioByIdUseCase,
    ListScenarioUseCase,
)
from src.scripts import seed_initial_data
from src.shared_kernel.application.use_cases.area.commands import (
    CreateAreaUseCase,
    DeleteAreaUseCase,
    RestoreAreaUseCase,
    UpdateAreaUseCase,
)
from src.shared_kernel.application.use_cases.area.queries import (
    GetAreaByIdUseCase,
    ListAreaUseCase,
)
from src.shared_kernel.application.use_cases.organizational_unit.commands import (
    CreateOrganizationalUnitUseCase,
    DeleteOrganizationalUnitUseCase,
    RestoreOrganizationalUnitUseCase,
    UpdateOrganizationalUnitUseCase,
)
from src.shared_kernel.application.use_cases.organizational_unit.queries import (
    GetOrganizationalUnitByIdUseCase,
    GetOrganizationalUnitByParentIdUseCase,
    ListOrganizationalUnitUseCase,
)
from src.shared_kernel.infrastructure.mappers import (
    AreaMapper,
)
from src.shared_kernel.infrastructure.models import AreaModel
from src.shared_kernel.infrastructure.repositories import (
    OrganizationalUnitRepository,
)
from src.tenant_management.application.use_cases.plan.commands import CreatePlanUseCase
from src.tenant_management.application.use_cases.plan.queries import ListPlansUseCase
from src.tenant_management.application.use_cases.tenant.commands import (
    UpdateTenantStatusUseCase,
)
from src.tenant_management.application.use_cases.tenant.queries import (
    ListTenantsUseCase,
)
from src.tenant_management.domain.entities import Tenant
from src.tenant_management.domain.value_objects import TenantStatus
from src.tenant_management.infrastructure.models import TenantModel
from tests.fakes import (
    AreaInMemoryRepository,
    DummyEntity,
    OrganizationalUnitInMemoryRepository,
    PermissionInMemoryRepository,
    PlanInMemoryRepository,
    RoleInMemoryRepository,
    ScenarioInMemoryRepository,
    TenantInMemoryRepository,
    UserInMemoryRepository,
)

# --- ENVIRONMENT VARIABLE LOGIC ---

# 1. Load the .env file into OS environment variables
load_dotenv()

# 2. Read the environment variable. Default is 'true' (use in-memory).
USE_IN_MEMORY_DB = os.getenv("TEST_IN_MEMORY", "true").lower() in ("true", "1", "t")

DB_FILE_PATH = "test.sqlite3"  # Name of the physical test file
CONNECT_ARGS = {"check_same_thread": False}
POOLCLASS: type[Pool] = NullPool  # Default pool for files

if USE_IN_MEMORY_DB:
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    # StaticPool is ESSENTIAL for :memory: to work with TestClient
    POOLCLASS = StaticPool
    print("\n--- Running tests with IN-MEMORY database (from .env) ---")
else:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE_PATH}"
    print(f"\n--- Running tests with FILE database ({DB_FILE_PATH}) (from .env) ---")


@pytest.fixture(autouse=True)
def mock_email_validator(monkeypatch):
    """
    Mock email_validator.validate_email to bypass
    DNS checks and return the input email as normalized.
    """

    def mock_validate(email, **kwargs):
        mock_result = MagicMock()
        mock_result.normalized = email
        return mock_result

    monkeypatch.setattr(
        "src.identity_access_management.domain.entities.user.validate_email",
        mock_validate,
    )
    return mock_validate


@pytest.fixture
def anyio_backend():
    """
    Fixture to specify the backend for anyio tests.
    """
    return "asyncio"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=CONNECT_ARGS,
    poolclass=POOLCLASS,  # Use the dynamic poolclass
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session")
def setup_database():
    """
    Creates the database tables once per test session.
    If using a file, deletes it at the end.
    """

    Base.metadata.create_all(bind=engine)
    yield
    # Only delete the file if we are not using in-memory
    if not USE_IN_MEMORY_DB:
        os.remove(DB_FILE_PATH)


@pytest.fixture(scope="function")
def db_session_for_test(setup_database) -> Generator[Session]:
    """
    Creates ONE transaction for each test, seeds data, flushes,
    and rolls back at the end.
    """

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    seed_initial_data(session)

    session.flush()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session_for_test: Session) -> Generator[TestClient, Any, Any]:
    """
    Creates a TestClient for each test, using the correct test session.
    """

    def override_get_db_session_for_test() -> Generator[Session]:
        yield db_session_for_test

    app.dependency_overrides[get_db_session] = override_get_db_session_for_test
    yield TestClient(app)
    app.dependency_overrides.clear()


# --- NEW DATA FIXTURES ---
@pytest.fixture(scope="function")
def default_tenant(db_session_for_test: Session) -> TenantModel:
    """
    Provides the default 'System Tenant' (TenantModel) created by seeding.
    """

    tenant = (
        db_session_for_test.query(TenantModel).filter_by(name="System Tenant").first()
    )
    assert tenant is not None, "Seeding of 'System Tenant' failed."
    return tenant


@pytest.fixture(scope="function")
def admin_user_model(
    db_session_for_test: Session,
    default_tenant: TenantModel,
) -> UserModel:
    """
    Provides the 'admin' UserModel created by seeding.
    """

    user = (
        db_session_for_test.query(UserModel)
        .filter_by(username="admin", tenant_id=default_tenant.id)
        .first()
    )
    assert user is not None, "Seeding of 'admin' user failed."
    return user


@pytest.fixture(scope="function")
def guest_user_model(
    db_session_for_test: Session,
    default_tenant: TenantModel,
) -> UserModel:
    """
    Provides the 'guest' UserModel created by seeding.
    """

    user = (
        db_session_for_test.query(UserModel)
        .filter_by(username="guest", tenant_id=default_tenant.id)
        .first()
    )

    assert user is not None, "Seeding of 'guest' user failed."
    return user


@pytest.fixture(scope="function")
def admin_actor(admin_user_model: UserModel) -> UserEntity:
    """
    Returns the 'admin' User (Domain Entity) to be used as an actor in use cases.
    """

    return UserMapper.to_entity(admin_user_model)


@pytest.fixture(scope="function")
def guest_actor(guest_user_model: UserModel) -> UserEntity:
    """
    Returns the 'guest' User (Domain Entity) to be used as an actor in use cases.
    """

    return UserMapper.to_entity(guest_user_model)


@pytest.fixture(scope="function")
def admin_token(client: TestClient) -> str:
    """
    Logs in as 'admin' and returns an access token.
    """

    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "foresight_admin"},
    )
    assert response.status_code == 200, f"Failed to get admin token: {response.json()}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def guest_token(client: TestClient) -> str:
    """
    Logs in as 'guest' and returns an access token.
    """

    response = client.post(
        "/auth/token",
        data={"username": "guest", "password": "foresight_guest"},
    )
    assert response.status_code == 200, f"Failed to get guest token: {response.json()}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def default_tenant_id(default_tenant: TenantModel) -> str:
    """
    Returns the tenant ID to be used.
    """

    return str(default_tenant.id)


@pytest.fixture(scope="function")
def admin_role_model(
    db_session_for_test: Session,
    default_tenant: TenantModel,
) -> RoleModel:
    """
    Provides the 'admin' RoleModel created by seeding.
    """
    role = (
        db_session_for_test.query(RoleModel)
        .filter_by(
            name="admin",
            tenant_id=default_tenant.id,
        )
        .first()
    )
    assert role is not None, "Seeding of 'admin' role failed."
    return role


@pytest.fixture(scope="function")
def guest_role_model(
    db_session_for_test: Session,
    default_tenant: TenantModel,
) -> RoleModel:
    """
    Provides the 'guest' RoleModel created by seeding.
    """
    role = (
        db_session_for_test.query(RoleModel)
        .filter_by(
            name="guest",
            tenant_id=default_tenant.id,
        )
        .first()
    )
    assert role is not None, "Seeding of 'guest' role failed."
    return role


@pytest.fixture(scope="function")
def admin_role(admin_role_model: RoleModel) -> RoleEntity:
    """
    Returns the 'admin' Role (Domain Entity) to be used as an role in use cases.
    """

    return RoleMapper.to_entity(admin_role_model)


@pytest.fixture(scope="function")
def guest_role(guest_role_model: RoleModel) -> RoleEntity:
    """
    Returns the 'guest' Role (Domain Entity) to be used as an role in use cases.
    """

    return RoleMapper.to_entity(guest_role_model)


# --- CONSOLIDATED FIXTURES ---


# API Auth Dependency Fixtures
@pytest.fixture
def auth_dependency_mock_session():
    """
    Fixture for a mock database session.
    """
    return Mock()


@pytest.fixture
def auth_dependency_mock_provider():
    """
    Fixture for a mock authentication provider.
    """
    provider = Mock()
    provider.get_user_from_token = AsyncMock()
    return provider


# API Authorization Dependency Fixtures
@pytest.fixture
def authorization_dependency_mock_user():
    """
    Fixture for a mock user.
    """
    return Mock(spec=User)


# API Local Provider Fixtures
@pytest.fixture
def local_auth_provider_mock_repo():
    """
    Fixture for a mock repository.
    """
    return Mock()


@pytest.fixture
def local_auth_provider(local_auth_provider_mock_repo):
    """
    Fixture for the LocalAuthenticationProvider.
    """
    return LocalAuthenticationProvider(local_auth_provider_mock_repo)


# Core Repository Fixtures
@pytest.fixture
def sqlalchemy_area_repository(db_session_for_test):
    """
    Fixture to provide a repository instance for testing.
    """
    return SQLAlchemyRepository(
        db_session_for_test,
        AreaModel,
        AreaMapper(),
    )


@pytest.fixture
def dummy_in_memory_repository():
    """
    Fixture for an in-memory repository.
    """
    return InMemoryRepository()


# Core Generic Use Case Fixtures
@pytest.fixture
def generic_delete_entity_id():
    """
    Fixture for an entity ID.
    """
    return uuid4()


@pytest.fixture
def generic_delete_use_case(dummy_in_memory_repository, generic_delete_entity_id):
    """
    Fixture for a delete use case.
    """
    return GenericDeleteUseCase[DummyEntity](
        dummy_in_memory_repository,
        AppPermission.USER_DELETE,
        EntityNotFoundError,
        f"DummyEntity with id={generic_delete_entity_id} not found",
    )


@pytest.fixture
def generic_get_by_id_use_case(dummy_in_memory_repository):
    """
    Fixture for a get by id use case.
    """
    return GenericGetByIdUseCase[DummyEntity](
        dummy_in_memory_repository,
        AppPermission.USER_READ,
        EntityNotFoundError,
        "DummyEntity with id={id} not found",
    )


@pytest.fixture
def generic_list_use_case(dummy_in_memory_repository):
    """
    Fixture for a list use case.
    """
    return GenericListUseCase[DummyEntity](
        dummy_in_memory_repository,
        AppPermission.USER_READ,
    )


# --- COMMON REPOSITORY FIXTURES ---


@pytest.fixture
def user_in_memory_repo():
    """Fixture that returns a UserInMemoryRepository."""
    return UserInMemoryRepository()


@pytest.fixture
def role_in_memory_repo():
    """Fixture that returns a RoleInMemoryRepository."""
    return RoleInMemoryRepository()


@pytest.fixture
def permission_in_memory_repo():
    """Fixture that returns a PermissionInMemoryRepository."""
    return PermissionInMemoryRepository()


@pytest.fixture
def plan_in_memory_repo():
    """Fixture that returns a PlanInMemoryRepository."""
    return PlanInMemoryRepository()


@pytest.fixture
def tenant_in_memory_repo():
    """Fixture that returns a TenantInMemoryRepository."""
    return TenantInMemoryRepository()


@pytest.fixture
def area_in_memory_repo():
    """Fixture that returns an AreaInMemoryRepository."""
    return AreaInMemoryRepository()


@pytest.fixture
def scenario_in_memory_repo():
    """Fixture that returns a ScenarioInMemoryRepository."""
    return ScenarioInMemoryRepository()


@pytest.fixture
def organizational_unit_in_memory_repo():
    """Fixture that returns an OrganizationalUnitInMemoryRepository."""
    return OrganizationalUnitInMemoryRepository()


@pytest.fixture(scope="function")
def permission_sqlalchemy_repo(db_session_for_test):
    """Fixture that returns a PermissionRepository."""
    return PermissionRepository(db_session_for_test)


@pytest.fixture(scope="function")
def user_sqlalchemy_repo(db_session_for_test):
    """Fixture that returns a UserRepository."""
    return UserRepository(db_session_for_test)


@pytest.fixture(scope="function")
def role_sqlalchemy_repo(db_session_for_test):
    """Fixture that returns a RoleRepository."""
    return RoleRepository(db_session_for_test)


# --- IAM USER USE CASE FIXTURES ---


@pytest.fixture
def authenticate_user_use_case(user_in_memory_repo):
    """Fixture for AuthenticateUserUseCase."""
    return AuthenticateUserUseCase(repository=user_in_memory_repo)


@pytest.fixture
def update_user_profile_use_case(user_in_memory_repo):
    """Fixture for UpdateUserProfileUseCase."""
    return UpdateUserProfileUseCase(user_in_memory_repo)


@pytest.fixture
def create_user_use_case(user_in_memory_repo, role_in_memory_repo):
    """Fixture for CreateUserUseCase."""
    return CreateUserUseCase(user_in_memory_repo, role_in_memory_repo)


@pytest.fixture
def restore_user_use_case(user_in_memory_repo):
    """Fixture for RestoreUserUseCase."""
    return RestoreUserUseCase(repository=user_in_memory_repo)


@pytest.fixture
def set_user_roles_use_case(user_in_memory_repo, role_in_memory_repo):
    """Fixture for SetUserRolesUseCase."""
    return SetUserRolesUseCase(
        user_repository=user_in_memory_repo, role_repository=role_in_memory_repo
    )


@pytest.fixture
def delete_user_use_case(user_in_memory_repo):
    """Fixture for DeleteUserUseCase."""
    return DeleteUserUseCase(repository=user_in_memory_repo)


@pytest.fixture
def change_password_use_case(user_in_memory_repo):
    """Fixture for ChangePasswordUseCase."""
    return ChangePasswordUseCase(user_in_memory_repo)


@pytest.fixture
def get_user_by_id_use_case(user_in_memory_repo):
    """Fixture for GetUserByIdUseCase."""
    return GetUserByIdUseCase(repository=user_in_memory_repo)


@pytest.fixture
def list_user_use_case(user_in_memory_repo):
    """Fixture for ListUserUseCase."""
    return ListUserUseCase(repository=user_in_memory_repo)


@pytest.fixture
def set_user_permissions_use_case(user_in_memory_repo, permission_in_memory_repo):
    """Fixture for SetUserPermissionsUseCase."""
    return SetUserPermissionsUseCase(
        user_repository=user_in_memory_repo,
        permission_repository=permission_in_memory_repo,
    )


@pytest.fixture
def onboarding_use_case(
    plan_in_memory_repo,
    tenant_in_memory_repo,
    role_in_memory_repo,
    user_in_memory_repo,
    permission_in_memory_repo,
):
    """Fixture for OnboardingUseCase."""
    return OnboardingUseCase(
        plan_repository=plan_in_memory_repo,
        tenant_repository=tenant_in_memory_repo,
        role_repository=role_in_memory_repo,
        user_repository=user_in_memory_repo,
        permission_repository=permission_in_memory_repo,
    )


# --- SHARED KERNEL USE CASE FIXTURES ---


@pytest.fixture
def create_area_use_case(area_in_memory_repo):
    """Fixture for CreateAreaUseCase."""
    return CreateAreaUseCase(area_in_memory_repo)


@pytest.fixture
def delete_area_use_case(area_in_memory_repo):
    """Fixture for DeleteAreaUseCase."""
    return DeleteAreaUseCase(area_in_memory_repo)


@pytest.fixture
def restore_area_use_case(area_in_memory_repo):
    """Fixture for RestoreAreaUseCase."""
    return RestoreAreaUseCase(area_in_memory_repo)


@pytest.fixture
def update_area_use_case(area_in_memory_repo):
    """Fixture for UpdateAreaUseCase."""
    return UpdateAreaUseCase(area_in_memory_repo)


@pytest.fixture
def get_area_by_id_use_case(area_in_memory_repo):
    """Fixture for GetAreaByIdUseCase."""
    return GetAreaByIdUseCase(area_in_memory_repo)


@pytest.fixture
def list_area_use_case(area_in_memory_repo):
    """Fixture for ListAreaUseCase."""
    return ListAreaUseCase(area_in_memory_repo)


@pytest.fixture
def create_scenario_use_case(scenario_in_memory_repo):
    """Fixture for CreateScenarioUseCase."""
    return CreateScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def delete_scenario_use_case(scenario_in_memory_repo):
    """Fixture for DeleteScenarioUseCase."""
    return DeleteScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def lock_scenario_use_case(scenario_in_memory_repo):
    """Fixture for LockScenarioUseCase."""
    return LockScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def restore_scenario_use_case(scenario_in_memory_repo):
    """Fixture for RestoreScenarioUseCase."""
    return RestoreScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def unlock_scenario_use_case(scenario_in_memory_repo):
    """Fixture for UnlockScenarioUseCase."""
    return UnlockScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def update_scenario_use_case(scenario_in_memory_repo):
    """Fixture for UpdateScenarioUseCase."""
    return UpdateScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def get_scenario_by_id_use_case(scenario_in_memory_repo):
    """Fixture for GetScenarioByIdUseCase."""
    return GetScenarioByIdUseCase(scenario_in_memory_repo)


@pytest.fixture
def list_scenario_use_case(scenario_in_memory_repo):
    """Fixture for ListScenarioUseCase."""
    return ListScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def create_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture for CreateOrganizationalUnitUseCase."""
    return CreateOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def delete_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture for DeleteOrganizationalUnitUseCase."""
    return DeleteOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def restore_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture for RestoreOrganizationalUnitUseCase."""
    return RestoreOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def update_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture for UpdateOrganizationalUnitUseCase."""
    return UpdateOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def get_organizational_unit_by_id_use_case(organizational_unit_in_memory_repo):
    """Fixture for GetOrganizationalUnitByIdUseCase."""
    return GetOrganizationalUnitByIdUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def get_organizational_unit_by_parent_id_use_case(organizational_unit_in_memory_repo):
    """Fixture for GetOrganizationalUnitByParentIdUseCase."""
    return GetOrganizationalUnitByParentIdUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def list_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture for ListOrganizationalUnitUseCase."""
    return ListOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


# --- TENANT MANAGEMENT USE CASE FIXTURES ---


@pytest.fixture
def create_plan_use_case(plan_in_memory_repo):
    """Fixture for CreatePlanUseCase."""
    return CreatePlanUseCase(plan_in_memory_repo)


@pytest.fixture
def list_plans_use_case(plan_in_memory_repo):
    """Fixture for ListPlansUseCase."""
    return ListPlansUseCase(plan_in_memory_repo)


@pytest.fixture
def update_tenant_status_use_case(tenant_in_memory_repo):
    """Fixture for UpdateTenantStatusUseCase."""
    return UpdateTenantStatusUseCase(tenant_in_memory_repo)


@pytest.fixture
def list_tenants_use_case(tenant_in_memory_repo):
    """Fixture for ListTenantsUseCase."""
    return ListTenantsUseCase(tenant_in_memory_repo)


# --- GENERIC MOCK FIXTURES ---


@pytest.fixture
def mock_user_repository():
    """Fixture that returns a mock user repository."""
    return Mock()


@pytest.fixture
def mock_role_repository():
    """Fixture that returns a mock role repository."""
    return Mock()


@pytest.fixture
def mock_permission_repository():
    """Fixture that returns a mock permission repository."""
    return Mock()


# --- IAM ROLE AND PERMISSION USE CASE FIXTURES ---


@pytest.fixture
def create_role_use_case(role_in_memory_repo, permission_in_memory_repo):
    """Fixture for CreateRoleUseCase."""
    return CreateRoleUseCase(role_in_memory_repo, permission_in_memory_repo)


@pytest.fixture
def delete_role_use_case_iam(role_in_memory_repo, user_in_memory_repo):
    """Fixture for DeleteRoleUseCase (IAM)."""
    return DeleteRoleUseCase_IAM(role_in_memory_repo, user_in_memory_repo)


@pytest.fixture
def restore_role_use_case_iam(role_in_memory_repo):
    """Fixture for RestoreRoleUseCase (IAM)."""
    return RestoreRoleUseCase_IAM(role_in_memory_repo)


@pytest.fixture
def update_role_use_case_iam(role_in_memory_repo):
    """Fixture for UpdateRoleUseCase (IAM)."""
    return UpdateRoleUseCase_IAM(repository=role_in_memory_repo)


@pytest.fixture
def get_role_by_id_use_case(role_in_memory_repo):
    """Fixture for GetRoleByIdUseCase."""
    return GetRoleByIdUseCase(repository=role_in_memory_repo)


@pytest.fixture
def list_role_use_case(role_in_memory_repo):
    """Fixture for ListRoleUseCase."""
    return ListRoleUseCase(repository=role_in_memory_repo)


@pytest.fixture
def set_role_permissions_use_case(role_in_memory_repo, permission_in_memory_repo):
    """Fixture for SetRolePermissionsUseCase."""
    return SetRolePermissionsUseCase(role_in_memory_repo, permission_in_memory_repo)


@pytest.fixture
def list_permissions_use_case(permission_in_memory_repo):
    """Fixture for ListPermissionsUseCase."""
    return ListPermissionsUseCase(repository=permission_in_memory_repo)


# --- REMAINING SPECIFIC FIXTURES ---


@pytest.fixture
def mock_tenant_entity():
    """Provides a valid Tenant entity mock for tests."""
    tenant = Mock(spec=Tenant)
    tenant.id = uuid4()
    tenant.name = "Test Tenant"
    tenant.plan_id = uuid4()
    tenant.status = TenantStatus.ACTIVE
    return tenant


@pytest.fixture(scope="function")
def organizational_unit_sqlalchemy_repo(db_session_for_test):
    """Fixture that returns an OrganizationalUnitRepository."""
    return OrganizationalUnitRepository(
        session=db_session_for_test,
    )


@pytest.fixture
def create_user_use_case_mocked(mock_user_repository, mock_role_repository):
    """Fixture for CreateUserUseCase initialized with mock repositories."""
    return CreateUserUseCase(mock_user_repository, mock_role_repository)


# --- FINANCE FIXTURES ---


@pytest.fixture
def brl_currency():
    """Fixture for BRL currency code."""
    return CurrencyCode(value="BRL")


@pytest.fixture
def usd_currency():
    """Fixture for USD currency code."""
    return CurrencyCode(value="USD")


@pytest.fixture
def money_brl_100(brl_currency):
    """Fixture for 100.00 BRL."""
    return Money(amount=Decimal("100.00"), currency=brl_currency)


@pytest.fixture
def money_usd_100(usd_currency):
    """Fixture for 100.00 USD."""
    return Money(amount=Decimal("100.00"), currency=usd_currency)

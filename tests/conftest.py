import os
from collections.abc import AsyncGenerator
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, Mock  # noqa: E402
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload
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

load_dotenv()

USE_IN_MEMORY_DB = os.getenv("TEST_IN_MEMORY", "true").lower() in ("true", "1", "t")

DB_FILE_PATH = "test.sqlite3"
CONNECT_ARGS = {"check_same_thread": False}
POOLCLASS: type[Pool] = NullPool

if USE_IN_MEMORY_DB:
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    POOLCLASS = StaticPool
    print("\n--- Running tests with IN-MEMORY database (from .env) ---")
else:
    SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///./{DB_FILE_PATH}"
    print(f"\n--- Running tests with FILE database ({DB_FILE_PATH}) (from .env) ---")


@pytest.fixture(autouse=True)
def mock_email_validator(monkeypatch):
    """Mock the validate_email function"""

    def mock_validate(email, **kwargs):
        """Mock the validate method"""

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
    """Fixture that represents backend"""

    return "asyncio"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=CONNECT_ARGS,
    poolclass=POOLCLASS,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
async def setup_database():
    """
    Creates the database tables once per test session.
    If using a file, deletes it at the end.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    if not USE_IN_MEMORY_DB:
        try:
            os.remove(DB_FILE_PATH)
        except OSError:
            pass


@pytest.fixture(scope="function")
async def db_session_for_test(setup_database) -> AsyncGenerator[AsyncSession]:
    """
    Creates ONE transaction for each test, seeds data,
    flushes and rolls back at the end.
    """

    connection = await engine.connect()
    transaction = await connection.begin()
    session = TestingSessionLocal(bind=connection)

    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())

    await seed_initial_data(session)  # type: ignore
    await session.flush()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture(scope="function")
async def client(db_session_for_test: AsyncSession) -> AsyncGenerator[AsyncClient]:
    """Creates an AsyncClient for each test."""

    async def override_get_db_session_for_test() -> AsyncGenerator[AsyncSession]:
        yield db_session_for_test

    app.dependency_overrides[get_db_session] = override_get_db_session_for_test

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def default_tenant(db_session_for_test: AsyncSession) -> TenantModel:
    """Fixture representing the default tenant."""

    stmt = select(TenantModel).filter_by(name="System Tenant")
    result = await db_session_for_test.execute(stmt)
    tenant = result.unique().scalar_one_or_none()
    assert tenant is not None, "Seeding of 'System Tenant' failed."
    return tenant


@pytest.fixture(scope="function")
async def admin_user_model(
    db_session_for_test: AsyncSession,
    default_tenant: TenantModel,
) -> UserModel:
    """Fixture representing the admin user."""

    stmt = (
        select(UserModel)
        .options(
            selectinload(UserModel.roles_rel).selectinload(RoleModel.permissions_rel)
        )
        .filter_by(username="admin", tenant_id=default_tenant.id)
    )
    result = await db_session_for_test.execute(stmt)
    user = result.unique().scalar_one_or_none()
    assert user is not None, "Seeding of 'admin' user failed."
    return user


@pytest.fixture(scope="function")
async def guest_user_model(
    db_session_for_test: AsyncSession,
    default_tenant: TenantModel,
) -> UserModel:
    """Fixture representing the guest user."""

    stmt = (
        select(UserModel)
        .options(
            selectinload(UserModel.roles_rel).selectinload(RoleModel.permissions_rel)
        )
        .filter_by(username="guest", tenant_id=default_tenant.id)
    )
    result = await db_session_for_test.execute(stmt)
    user = result.unique().scalar_one_or_none()
    assert user is not None, "Seeding of 'guest' user failed."
    return user


@pytest.fixture(scope="function")
def admin_actor(admin_user_model: UserModel) -> UserEntity:
    """Fixture representing the admin user."""

    return UserMapper.to_entity(admin_user_model)


@pytest.fixture(scope="function")
def guest_actor(guest_user_model: UserModel) -> UserEntity:
    """Fixture representing the guest user."""

    return UserMapper.to_entity(guest_user_model)


@pytest.fixture(scope="function")
async def admin_token(client: AsyncClient) -> str:
    """Fixture representing the admin token."""

    response = await client.post(
        "/auth/token",
        data={
            "username": "admin",
            "password": "foresight_admin",
        },
    )
    assert response.status_code == 200, f"Failed to get admin token: {response.json()}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
async def guest_token(client: AsyncClient) -> str:
    """Fixture representing the guest token."""

    response = await client.post(
        "/auth/token",
        data={
            "username": "guest",
            "password": "foresight_guest",
        },
    )
    assert response.status_code == 200, f"Failed to get guest token: {response.json()}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def default_tenant_id(default_tenant: TenantModel) -> str:
    """Fixture representing the default tenant id."""

    return str(default_tenant.id)


@pytest.fixture(scope="function")
async def admin_role_model(
    db_session_for_test: AsyncSession,
    default_tenant: TenantModel,
) -> RoleModel:
    """Fixture representing the admin role."""

    stmt = (
        select(RoleModel)
        .options(selectinload(RoleModel.permissions_rel))
        .filter_by(name="admin", tenant_id=default_tenant.id)
    )
    result = await db_session_for_test.execute(stmt)
    role = result.unique().scalar_one_or_none()
    assert role is not None, "Seeding of 'admin' role failed."
    return role


@pytest.fixture(scope="function")
async def guest_role_model(
    db_session_for_test: AsyncSession,
    default_tenant: TenantModel,
) -> RoleModel:
    """Fixture representing the guest role."""

    stmt = (
        select(RoleModel)
        .options(selectinload(RoleModel.permissions_rel))
        .filter_by(name="guest", tenant_id=default_tenant.id)
    )
    result = await db_session_for_test.execute(stmt)
    role = result.unique().scalar_one_or_none()
    assert role is not None, "Seeding of 'guest' role failed."
    return role


@pytest.fixture(scope="function")
def admin_role(admin_role_model: RoleModel) -> RoleEntity:
    """Fixture representing the admin role."""

    return RoleMapper.to_entity(admin_role_model)


@pytest.fixture(scope="function")
def guest_role(guest_role_model: RoleModel) -> RoleEntity:
    """Fixture representing the guest role."""

    return RoleMapper.to_entity(guest_role_model)


@pytest.fixture
def auth_dependency_mock_session():
    """Fixture mocking the auth dependency session"""

    return Mock()


@pytest.fixture
def auth_dependency_mock_provider():
    """Fixture mocking the auth dependency provider"""

    provider = Mock()
    provider.get_user_from_token = AsyncMock()
    return provider


@pytest.fixture
def authorization_dependency_mock_user():
    """Fixture mocking the authorization dependency user"""

    return Mock(spec=User)


@pytest.fixture
def local_auth_provider_mock_repo():
    """Fixture mocking the local auth provider repository"""

    return Mock()


@pytest.fixture
def local_auth_provider(local_auth_provider_mock_repo):
    """Fixture mocking the local auth provider"""

    return LocalAuthenticationProvider(local_auth_provider_mock_repo)


@pytest.fixture
def sqlalchemy_area_repository(db_session_for_test):
    """Fixture representing the area repository."""

    return SQLAlchemyRepository(
        db_session_for_test,
        AreaModel,
        AreaMapper(),
    )


@pytest.fixture
def dummy_in_memory_repository():
    """Fixture representing the dummy in-memory repository."""

    return InMemoryRepository()


@pytest.fixture
def generic_delete_entity_id():
    """Fixture representing the generic delete entity id."""

    return uuid4()


@pytest.fixture
def generic_delete_use_case(dummy_in_memory_repository, generic_delete_entity_id):
    """Fixture representing the generic delete use case."""

    return GenericDeleteUseCase[DummyEntity](
        dummy_in_memory_repository,
        AppPermission.USER_DELETE,
        EntityNotFoundError,
        f"DummyEntity with id={generic_delete_entity_id} not found",
    )


@pytest.fixture
def generic_get_by_id_use_case(dummy_in_memory_repository):
    """Fixture representing the generic get by id use case."""

    return GenericGetByIdUseCase[DummyEntity](
        dummy_in_memory_repository,
        AppPermission.USER_READ,
        EntityNotFoundError,
        "DummyEntity with id={id} not found",
    )


@pytest.fixture
def generic_list_use_case(dummy_in_memory_repository):
    """Fixture representing the generic list use case."""

    return GenericListUseCase[DummyEntity](
        dummy_in_memory_repository,
        AppPermission.USER_READ,
    )


@pytest.fixture
def user_in_memory_repo():
    """Fixture representing the user in-memory repository."""

    return UserInMemoryRepository()


@pytest.fixture
def role_in_memory_repo():
    """Fixture representing the role in-memory repository."""

    return RoleInMemoryRepository()


@pytest.fixture
def permission_in_memory_repo():
    """Fixture representing the permission in-memory repository."""

    return PermissionInMemoryRepository()


@pytest.fixture
def plan_in_memory_repo():
    """Fixture representing the plan in-memory repository."""

    return PlanInMemoryRepository()


@pytest.fixture
def tenant_in_memory_repo():
    """Fixture representing the tenant in-memory repository."""

    return TenantInMemoryRepository()


@pytest.fixture
def area_in_memory_repo():
    """Fixture representing the area in-memory repository."""

    return AreaInMemoryRepository()


@pytest.fixture
def scenario_in_memory_repo():
    """Fixture representing the scenario in-memory repository."""

    return ScenarioInMemoryRepository()


@pytest.fixture
def organizational_unit_in_memory_repo():
    """Fixture representing the organizational unit in-memory repository."""

    return OrganizationalUnitInMemoryRepository()


@pytest.fixture(scope="function")
def permission_sqlalchemy_repo(db_session_for_test):
    """Fixture representing the permission repository."""

    return PermissionRepository(db_session_for_test)


@pytest.fixture(scope="function")
def user_sqlalchemy_repo(db_session_for_test):
    """Fixture representing the user repository."""

    return UserRepository(db_session_for_test)


@pytest.fixture(scope="function")
def role_sqlalchemy_repo(db_session_for_test):
    """Fixture representing the role repository."""

    return RoleRepository(db_session_for_test)


@pytest.fixture
def authenticate_user_use_case(user_in_memory_repo):
    """Fixture representing the authenticate user use case."""

    return AuthenticateUserUseCase(repository=user_in_memory_repo)


@pytest.fixture
def update_user_profile_use_case(user_in_memory_repo):
    """Fixture representing the update user profile use case."""

    return UpdateUserProfileUseCase(user_in_memory_repo)


@pytest.fixture
def create_user_use_case(user_in_memory_repo, role_in_memory_repo):
    """Fixture representing the create user use case."""

    return CreateUserUseCase(user_in_memory_repo, role_in_memory_repo)


@pytest.fixture
def restore_user_use_case(user_in_memory_repo):
    """Fixture representing the restore user use case."""

    return RestoreUserUseCase(repository=user_in_memory_repo)


@pytest.fixture
def set_user_roles_use_case(user_in_memory_repo, role_in_memory_repo):
    """Fixture representing the set user roles use case."""

    return SetUserRolesUseCase(
        user_repository=user_in_memory_repo,
        role_repository=role_in_memory_repo,
    )


@pytest.fixture
def delete_user_use_case(user_in_memory_repo):
    """Fixture representing the delete user use case."""

    return DeleteUserUseCase(repository=user_in_memory_repo)


@pytest.fixture
def change_password_use_case(user_in_memory_repo):
    """Fixture representing the change password use case."""

    return ChangePasswordUseCase(user_in_memory_repo)


@pytest.fixture
def get_user_by_id_use_case(user_in_memory_repo):
    """Fixture representing the get user by id use case."""

    return GetUserByIdUseCase(repository=user_in_memory_repo)


@pytest.fixture
def list_user_use_case(user_in_memory_repo):
    """Fixture representing the list user use case."""

    return ListUserUseCase(repository=user_in_memory_repo)


@pytest.fixture
def set_user_permissions_use_case(user_in_memory_repo, permission_in_memory_repo):
    """Fixture representing the set user permissions use case."""

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
    """Fixture representing the onboarding use case."""

    return OnboardingUseCase(
        plan_repository=plan_in_memory_repo,
        tenant_repository=tenant_in_memory_repo,
        role_repository=role_in_memory_repo,
        user_repository=user_in_memory_repo,
        permission_repository=permission_in_memory_repo,
    )


@pytest.fixture
def create_area_use_case(area_in_memory_repo):
    """Fixture representing the create area use case."""

    return CreateAreaUseCase(area_in_memory_repo)


@pytest.fixture
def delete_area_use_case(area_in_memory_repo):
    """Fixture representing the delete area use case."""

    return DeleteAreaUseCase(area_in_memory_repo)


@pytest.fixture
def restore_area_use_case(area_in_memory_repo):
    """Fixture representing the restore area use case."""

    return RestoreAreaUseCase(area_in_memory_repo)


@pytest.fixture
def update_area_use_case(area_in_memory_repo):
    """Fixture representing the update area use case."""

    return UpdateAreaUseCase(area_in_memory_repo)


@pytest.fixture
def get_area_by_id_use_case(area_in_memory_repo):
    """Fixture representing the get area by id use case."""

    return GetAreaByIdUseCase(area_in_memory_repo)


@pytest.fixture
def list_area_use_case(area_in_memory_repo):
    """Fixture representing the list area use case."""

    return ListAreaUseCase(area_in_memory_repo)


@pytest.fixture
def create_scenario_use_case(scenario_in_memory_repo):
    """Fixture representing the create scenario use case."""

    return CreateScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def delete_scenario_use_case(scenario_in_memory_repo):
    """Fixture representing the delete scenario use case."""

    return DeleteScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def lock_scenario_use_case(scenario_in_memory_repo):
    """Fixture representing the lock scenario use case."""

    return LockScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def restore_scenario_use_case(scenario_in_memory_repo):
    """Fixture representing the restore scenario use case."""

    return RestoreScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def unlock_scenario_use_case(scenario_in_memory_repo):
    """Fixture representing the unlock scenario use case."""

    return UnlockScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def update_scenario_use_case(scenario_in_memory_repo):
    """Fixture representing the update scenario use case."""

    return UpdateScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def get_scenario_by_id_use_case(scenario_in_memory_repo):
    """Fixture representing the get scenario by id use case."""

    return GetScenarioByIdUseCase(scenario_in_memory_repo)


@pytest.fixture
def list_scenario_use_case(scenario_in_memory_repo):
    """Fixture representing the list scenario use case."""

    return ListScenarioUseCase(scenario_in_memory_repo)


@pytest.fixture
def create_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture representing the create organizational unit use case."""

    return CreateOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def delete_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture representing the delete organizational unit use case."""

    return DeleteOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def restore_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture representing the restore organizational unit use case."""

    return RestoreOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def update_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture representing the update organizational unit use case."""

    return UpdateOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def get_organizational_unit_by_id_use_case(organizational_unit_in_memory_repo):
    """Fixture representing the get organizational unit by id use case."""

    return GetOrganizationalUnitByIdUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def get_organizational_unit_by_parent_id_use_case(organizational_unit_in_memory_repo):
    """Fixture representing the get organizational unit by parent id use case."""

    return GetOrganizationalUnitByParentIdUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def list_organizational_unit_use_case(organizational_unit_in_memory_repo):
    """Fixture representing the list organizational unit use case."""

    return ListOrganizationalUnitUseCase(organizational_unit_in_memory_repo)


@pytest.fixture
def create_plan_use_case(plan_in_memory_repo):
    """Fixture representing the create plan use case."""

    return CreatePlanUseCase(plan_in_memory_repo)


@pytest.fixture
def list_plans_use_case(plan_in_memory_repo):
    """Fixture representing the list plans use case."""

    return ListPlansUseCase(plan_in_memory_repo)


@pytest.fixture
def update_tenant_status_use_case(tenant_in_memory_repo):
    """Fixture representing the update tenant status use case."""

    return UpdateTenantStatusUseCase(tenant_in_memory_repo)


@pytest.fixture
def list_tenants_use_case(tenant_in_memory_repo):
    """Fixture representing the list tenants use case."""

    return ListTenantsUseCase(tenant_in_memory_repo)


@pytest.fixture
def mock_user_repository():
    """Fixture mocking the user repository"""

    return Mock()


@pytest.fixture
def mock_role_repository():
    """Fixture mocking the role repository"""

    return Mock()


@pytest.fixture
def mock_permission_repository():
    """Fixture mocking the permission repository"""

    return Mock()


@pytest.fixture
def create_role_use_case(role_in_memory_repo, permission_in_memory_repo):
    """Fixture representing the create role use case."""

    return CreateRoleUseCase(role_in_memory_repo, permission_in_memory_repo)


@pytest.fixture
def delete_role_use_case_iam(role_in_memory_repo, user_in_memory_repo):
    """Fixture representing the delete role use case."""

    return DeleteRoleUseCase_IAM(role_in_memory_repo, user_in_memory_repo)


@pytest.fixture
def restore_role_use_case_iam(role_in_memory_repo):
    """Fixture representing the restore role use case."""

    return RestoreRoleUseCase_IAM(role_in_memory_repo)


@pytest.fixture
def update_role_use_case_iam(role_in_memory_repo):
    """Fixture representing the update role use case."""

    return UpdateRoleUseCase_IAM(repository=role_in_memory_repo)


@pytest.fixture
def get_role_by_id_use_case(role_in_memory_repo):
    """Fixture representing the get role by id use case."""

    return GetRoleByIdUseCase(repository=role_in_memory_repo)


@pytest.fixture
def list_role_use_case(role_in_memory_repo):
    """Fixture representing the list role use case."""

    return ListRoleUseCase(repository=role_in_memory_repo)


@pytest.fixture
def set_role_permissions_use_case(role_in_memory_repo, permission_in_memory_repo):
    """Fixture representing the set role permissions use case."""

    return SetRolePermissionsUseCase(role_in_memory_repo, permission_in_memory_repo)


@pytest.fixture
def list_permissions_use_case(permission_in_memory_repo):
    """Fixture representing the list permissions use case."""

    return ListPermissionsUseCase(repository=permission_in_memory_repo)


@pytest.fixture
def mock_tenant_entity():
    """Fixture representing the mock tenant entity."""

    tenant = Mock(spec=Tenant)
    tenant.id = uuid4()
    tenant.name = "Test Tenant"
    tenant.plan_id = uuid4()
    tenant.status = TenantStatus.ACTIVE
    return tenant


@pytest.fixture(scope="function")
def organizational_unit_sqlalchemy_repo(db_session_for_test):
    """Fixture representing the organizational unit repository."""

    return OrganizationalUnitRepository(
        session=db_session_for_test,
    )


@pytest.fixture
def create_user_use_case_mocked(mock_user_repository, mock_role_repository):
    """Fixture representing the create user use case."""

    return CreateUserUseCase(mock_user_repository, mock_role_repository)


@pytest.fixture
def brl_currency():
    """Fixture representing the Brazilian Real currency."""

    return CurrencyCode(value="BRL")


@pytest.fixture
def usd_currency():
    """Fixture representing the US Dollar currency."""

    return CurrencyCode(value="USD")


@pytest.fixture
def money_brl_100(brl_currency):
    """Fixture representing the Brazilian Real money."""

    return Money(amount=Decimal("100.00"), currency=brl_currency)


@pytest.fixture
def money_usd_100(usd_currency):
    """Fixture representing the US Dollar money."""

    return Money(amount=Decimal("100.00"), currency=usd_currency)

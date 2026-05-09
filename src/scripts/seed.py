from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.identity_access_management.domain.constants import AppPermission

# Import domain entities only for hashing password
from src.identity_access_management.domain.entities.user import hash_password

# Import SQLAlchemy models for querying AND adding
from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    RoleModel,
    UserModel,
)
from src.tenant_management.infrastructure.models import PlanModel, TenantModel


async def seed_initial_plan(db_session: AsyncSession) -> PlanModel:
    """
    Creates the default 'Standard' plan if it doesn't exist.
    Returns the PlanModel object.
    """
    print("Checking for initial plan...")
    # Query using the Model
    stmt = select(PlanModel).where(PlanModel.name == "Standard")

    result = await db_session.execute(stmt)
    plan = result.unique().scalar_one_or_none()

    if not plan:
        plan = PlanModel(name="Standard", price=0.01)
        db_session.add(plan)
        await db_session.flush()
        print("Plan 'Standard' created.")

    return plan


async def seed_initial_tenant(db_session: AsyncSession, plan_id: str) -> TenantModel:
    """
    Creates a default 'System Tenant' if it doesn't exist.
    Returns the TenantModel object.
    """
    print("Checking for initial tenant...")
    # Query using the Model
    stmt = select(TenantModel).where(TenantModel.name == "System Tenant")
    result = await db_session.execute(stmt)
    tenant = result.unique().scalar_one_or_none()

    if not tenant:
        tenant = TenantModel(name="System Tenant", plan_id=plan_id)
        db_session.add(tenant)
        await db_session.flush()
        print("Tenant 'System Tenant' created.")

    return tenant


async def seed_initial_roles(
    db_session: AsyncSession,
    tenant_id: str,
) -> dict[str, RoleModel]:
    """
    Creates initial 'admin' and 'guest' roles for the tenant if they don't exist.
    Queries using RoleModel.
    Returns a dictionary of the RoleModel objects.
    """
    print(f"Checking for initial roles for tenant {tenant_id}...")
    roles = {}

    admin_stmt = (
        select(RoleModel)
        .options(selectinload(RoleModel.permissions_rel))
        .where(
            RoleModel.name == "admin",
            RoleModel.tenant_id == tenant_id,
        )
    )

    guest_stmt = (
        select(RoleModel)
        .options(selectinload(RoleModel.permissions_rel))
        .where(
            RoleModel.name == "guest",
            RoleModel.tenant_id == tenant_id,
        )
    )

    admin_result = await db_session.execute(admin_stmt)
    guest_result = await db_session.execute(guest_stmt)

    admin_exists = admin_result.unique().scalar_one_or_none()
    guest_exists = guest_result.unique().scalar_one_or_none()
    # --- FIM DA CORREÇÃO ---

    if not admin_exists:
        admin_role_model = RoleModel(
            name="admin",
            description="Administrator with full access.",
            tenant_id=tenant_id,
        )
        db_session.add(admin_role_model)
        roles["admin"] = admin_role_model
        print("Role 'admin' created.")
    else:
        roles["admin"] = admin_exists

    if not guest_exists:
        guest_role_model = RoleModel(
            name="guest",
            description="User with limited permissions.",
            tenant_id=tenant_id,
        )
        db_session.add(guest_role_model)
        roles["guest"] = guest_role_model
        print("Role 'guest' created.")
    else:
        roles["guest"] = guest_exists

    await db_session.flush()
    print("Initial roles seeding completed.")
    return roles


async def seed_app_permissions(
    db_session: AsyncSession,
    admin_role: RoleModel,
    guest_role: RoleModel | None = None,
):
    """
    Create application permissions if they don't exist, using PermissionModel
    for queries. Assigns all permissions to the admin role.
    """
    print("Checking for app permissions...")
    permissions = AppPermission.get_all_permissions()
    admin_role_permissions = {p.codename for p in admin_role.permissions_rel}
    guest_role_permissions = (
        {p.codename for p in guest_role.permissions_rel} if guest_role else set()
    )

    guest_allowed_codenames = AppPermission.get_guest_permissions()

    for permission_codename in permissions:
        stmt = select(PermissionModel).where(
            PermissionModel.codename == permission_codename
        )

        result = await db_session.execute(stmt)

        permission_model = result.unique().scalar_one_or_none()

        if not permission_model:
            permission_model = PermissionModel(
                codename=permission_codename,
                description=(
                    f"Can {permission_codename.split(':')[1].replace('_', ' ')} "
                    f"{permission_codename.split(':')[0].replace('_', ' ')}"
                ),
            )
            db_session.add(permission_model)
            print(f"Permission '{permission_codename}' created.")

        if permission_codename not in admin_role_permissions:
            admin_role.permissions_rel.append(permission_model)
            print(f"Permission '{permission_codename}' set for role 'admin'.")

        if guest_role and permission_codename in guest_allowed_codenames:
            if permission_codename not in guest_role_permissions:
                guest_role.permissions_rel.append(permission_model)
                print(f"Permission '{permission_codename}' set for role 'guest'.")

    db_session.add(admin_role)
    if guest_role:
        db_session.add(guest_role)

    print("App permissions seeding completed.")


async def seed_initial_users(
    db_session: AsyncSession,
    tenant_id: str,
    roles: dict[str, RoleModel],
):
    """
    Creates initial 'admin' and 'guest' users for the tenant if they don't exist.
    Associates roles by querying RoleModel.
    """
    print(f"Checking for initial users for tenant {tenant_id}...")

    # --- CORREÇÃO AQUI: Query using UserModel ---
    admin_stmt = select(UserModel).where(
        UserModel.username == "admin",
        UserModel.tenant_id == tenant_id,
    )

    guest_stmt = select(UserModel).where(
        UserModel.username == "guest",
        UserModel.tenant_id == tenant_id,
    )

    admin_result = await db_session.execute(admin_stmt)
    guest_result = await db_session.execute(guest_stmt)

    admin_exists = admin_result.unique().scalar_one_or_none()
    guest_exists = guest_result.unique().scalar_one_or_none()
    # --- FIM DA CORREÇÃO ---
    users_to_create_data = {
        "admin": {"password": "foresight_admin", "role_key": "admin"},
        "guest": {"password": "foresight_guest", "role_key": "guest"},
    }

    if not admin_exists:
        data = users_to_create_data["admin"]
        admin_password: str = data["password"]
        admin_user_model = UserModel(
            username="admin",
            tenant_id=tenant_id,
            hashed_password=hash_password(admin_password),
            roles_rel=[roles["admin"]],
            is_active=True,
        )
        db_session.add(admin_user_model)
        print("User 'admin' created.")

    if not guest_exists:
        data = users_to_create_data["guest"]
        guest_password: str = data["password"]
        guest_user_model = UserModel(
            username="guest",
            tenant_id=tenant_id,
            hashed_password=hash_password(guest_password),
            roles_rel=[roles["guest"]],
            is_active=True,
        )
        db_session.add(guest_user_model)
        print("User 'guest' created.")

    print("Initial users seeding completed.")


async def seed_initial_data(db_session: AsyncSession):
    """
    Runs all seeding functions in the correct order to populate
    the database with initial data for a default tenant.
    """
    print("Starting database seeding process...")

    default_plan = await seed_initial_plan(db_session)
    default_tenant = await seed_initial_tenant(db_session, default_plan.id)  # type: ignore
    roles = await seed_initial_roles(db_session, default_tenant.id)  # type: ignore

    if "admin" in roles:
        guest_role = roles.get("guest")
        await seed_app_permissions(
            db_session,
            roles["admin"],
            guest_role,
        )

    await seed_initial_users(
        db_session,
        default_tenant.id,  # type: ignore
        roles,
    )  # type: ignore

    print("Database seeding finished.")

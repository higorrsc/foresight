from typing import Optional

from sqlalchemy.orm import Session

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


def seed_initial_plan(db_session: Session) -> PlanModel:
    """
    Creates the default 'Standard' plan if it doesn't exist.
    Returns the PlanModel object.
    """
    print("Checking for initial plan...")
    # Query using the Model
    plan = db_session.query(PlanModel).filter_by(name="Standard").first()

    if not plan:
        plan = PlanModel(name="Standard", price=0.01)
        db_session.add(plan)
        print("Plan 'Standard' created.")

    db_session.flush()
    return plan


def seed_initial_tenant(db_session: Session, plan_id: str) -> TenantModel:
    """
    Creates a default 'System Tenant' if it doesn't exist.
    Returns the TenantModel object.
    """
    print("Checking for initial tenant...")
    # Query using the Model
    tenant = db_session.query(TenantModel).filter_by(name="System Tenant").first()

    if not tenant:
        tenant = TenantModel(name="System Tenant", plan_id=plan_id)
        db_session.add(tenant)
        print("Tenant 'System Tenant' created.")

    db_session.flush()
    return tenant


def seed_initial_roles(db_session: Session, tenant_id: str) -> dict[str, RoleModel]:
    """
    Creates initial 'admin' and 'guest' roles for the tenant if they don't exist.
    Queries using RoleModel.
    Returns a dictionary of the RoleModel objects.
    """
    print(f"Checking for initial roles for tenant {tenant_id}...")
    roles = {}

    admin_exists = (
        db_session.query(RoleModel).filter_by(name="admin", tenant_id=tenant_id).first()
    )
    guest_exists = (
        db_session.query(RoleModel).filter_by(name="guest", tenant_id=tenant_id).first()
    )
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

    print("Initial roles seeding completed.")
    return roles


def seed_app_permissions(
    db_session: Session,
    admin_role: RoleModel,
    guest_role: Optional[RoleModel] = None,
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
        permission_model = (
            db_session.query(PermissionModel)
            .filter_by(codename=permission_codename)
            .first()
        )

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


def seed_initial_users(
    db_session: Session,
    tenant_id: str,
    roles: dict[str, RoleModel],
):
    """
    Creates initial 'admin' and 'guest' users for the tenant if they don't exist.
    Associates roles by querying RoleModel.
    """
    print(f"Checking for initial users for tenant {tenant_id}...")

    # --- CORREÇÃO AQUI: Query using UserModel ---
    admin_exists = (
        db_session.query(UserModel)
        .filter_by(username="admin", tenant_id=tenant_id)
        .first()
    )
    guest_exists = (
        db_session.query(UserModel)
        .filter_by(username="guest", tenant_id=tenant_id)
        .first()
    )
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


def seed_initial_data(db_session: Session):
    """
    Runs all seeding functions in the correct order to populate
    the database with initial data for a default tenant.
    """
    print("Starting database seeding process...")

    default_plan = seed_initial_plan(db_session)
    default_tenant = seed_initial_tenant(db_session, default_plan.id)  # type: ignore
    roles = seed_initial_roles(db_session, default_tenant.id)  # type: ignore

    if "admin" in roles:
        guest_role = roles.get("guest")
        seed_app_permissions(
            db_session,
            roles["admin"],
            guest_role,
        )

    seed_initial_users(db_session, default_tenant.id, roles)  # type: ignore

    print("Database seeding finished.")

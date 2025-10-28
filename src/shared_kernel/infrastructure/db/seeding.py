from sqlalchemy.orm import Session

from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    RoleModel,
    UserModel,
)


def seed_initial_roles(db_session: Session):
    """
    Creates initial roles 'admin' and 'guest' if they don't exist, using RoleModel for queries.
    """

    print("Checking for initial roles...")

    admin_exists = db_session.query(RoleModel).filter_by(name="admin").first()
    guest_exists = db_session.query(RoleModel).filter_by(name="guest").first()

    if not admin_exists:
        admin_role_model = RoleModel(
            name="admin",
            description="Administrator with full access.",
        )
        db_session.add(admin_role_model)
        print("Role 'admin' created.")

    if not guest_exists:
        guest_role_model = RoleModel(
            name="guest",
            description="User with limited permissions.",
        )
        db_session.add(guest_role_model)
        print("Role 'guest' created.")

    print("Initial roles seeding completed.")


def seed_initial_users(db_session: Session):
    """
    Creates initial users 'admin' and 'guest' if they don't exist, using UserModel for queries.
    Associates roles by querying RoleModel.
    """

    print("Checking for initial users...")

    admin_exists = db_session.query(UserModel).filter_by(username="admin").first()
    guest_exists = db_session.query(UserModel).filter_by(username="guest").first()

    users_to_create = {
        "admin": {"password": "foresight_admin", "roles": ["admin"]},
        "guest": {"password": "foresight_guest", "roles": ["guest"]},
    }

    if not admin_exists:
        data = users_to_create["admin"]
        roles = (
            db_session.query(RoleModel).filter(RoleModel.name.in_(data["roles"])).all()
        )
        if len(roles) != len(data["roles"]):
            print(f"Warning: Not all roles found for user 'admin': {data['roles']}")

        admin_user_model = UserModel(
            username="admin",
            hashed_password=hash_password(str(data["password"])),
            roles=roles,
        )
        db_session.add(admin_user_model)
        print("User 'admin' created.")

    if not guest_exists:
        data = users_to_create["guest"]
        roles = (
            db_session.query(RoleModel).filter(RoleModel.name.in_(data["roles"])).all()
        )
        if len(roles) != len(data["roles"]):
            print(f"Warning: Not all roles found for user 'guest': {data['roles']}")

        guest_user_model = UserModel(
            username="guest",
            hashed_password=hash_password(str(data["password"])),
            roles=roles,
        )
        db_session.add(guest_user_model)
        print("User 'guest' created.")

    print("Initial users seeding completed.")


def seed_app_permissions(db_session: Session):
    """
    Create application permissions if that doesn't exists, using PermissionModel for queries.
    """

    print("Checking for app permissions...")

    permissions = AppPermission.get_all_permissions()
    admin_role = db_session.query(RoleModel).filter_by(name="admin").first()

    for permission in permissions:
        permission_exists = (
            db_session.query(PermissionModel).filter_by(codename=permission).first()
        )
        if not permission_exists:
            permission_model = PermissionModel(
                codename=permission,
                description=f"Can {permission.split(":")[1]} {permission.split(':')[0]}",
            )
            db_session.add(permission_model)
            print(f"Permission '{permission}' created.")

            if admin_role:
                admin_role.permissions.append(permission_model)
                db_session.add(admin_role)
                print(f"Permission '{permission}' set for role 'admin'.")

    print("App permissions seeding completed.")

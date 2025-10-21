from sqlalchemy.orm import Session

from src.core.domain.entities import hash_password
from src.core.infrastructure.models import RoleModel, UserModel


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
    # else:
    # print("Role 'admin' already exists.")

    if not guest_exists:
        guest_role_model = RoleModel(
            name="guest",
            description="User with limited permissions.",
        )
        db_session.add(guest_role_model)
        print("Role 'guest' created.")
    # else:
    # print("Role 'guest' already exists.")

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
    # else:
    # print("User 'admin' already exists.")

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
    # else:
    # print("User 'guest' already exists.")

    print("Initial users seeding completed.")

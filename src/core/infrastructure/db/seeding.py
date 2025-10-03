from sqlalchemy.orm import Session

from src.core.domain.entities import Role, User, hash_password
from src.core.infrastructure.repositories import RoleRepository, UserRepository


def seed_initial_roles(db_session: Session):
    """
    Create initial roles 'admin' and 'guest' if they don't exist.
    """

    print("Checking for initial roles...")
    role_repo = RoleRepository(db_session)

    roles_to_create = {
        "admin": "Administrator with full access to the system.",
        "guest": "User with limited viewing permissions.",
    }

    for role_name, role_desc in roles_to_create.items():
        existing_role = role_repo.get_by_name(role_name)
        if not existing_role:
            new_role = Role(name=role_name, description=role_desc)
            role_repo.save(new_role)
            print(f"Role '{role_name}' created successfully.")
        else:
            print(f"Role '{role_name}' already exists.")

    print("Initial roles seeded successfully.")


def seed_initial_users(db_session: Session):
    """
    Create initial users 'admin' and 'guest' if they don't exist.
    """

    print("Checking for initial users...")
    user_repo = UserRepository(db_session)
    users_to_create = {
        "admin": {
            "password": "foresight_admin",
            "roles": ["admin"],
        },
        "guest": {
            "password": "foresight_guest",
            "roles": ["guest"],
        },
    }

    for username, data in users_to_create.items():
        if not user_repo.get_by_username(username):
            new_user = User(
                username=username,
                hashed_password=hash_password(data["password"]),
                roles=set(data["roles"]),
            )
            user_repo.save(new_user)
            print(f"User '{username}' created successfully.")
        else:
            print(f"User '{username}' already exists.")

    print("Initial users seeded successfully.")

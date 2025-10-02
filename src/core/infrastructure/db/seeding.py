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
        "admin": "foresight_admin",
        "guest": "foresight_guest",
    }

    for user_name, password in users_to_create.items():
        existing_user = user_repo.get_by_username(user_name)
        if not existing_user:
            new_user = User(
                username=user_name,
                hashed_password=hash_password(password),
                roles=[user_name],  # type: ignore
            )
            user_repo.save(new_user)
            print(f"User '{user_name}' created successfully.")
        else:
            print(f"User '{user_name}' already exists.")

    print("Initial users seeded successfully.")

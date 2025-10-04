from dataclasses import dataclass, field
from typing import Optional, Set

from email_validator import EmailNotValidError, validate_email
from passlib.context import CryptContext

from src.core.domain._shared import AbstractEntity, EntityValidationError

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@dataclass(kw_only=True, eq=False)
class User(AbstractEntity):
    """
    Entity representing a user in the system.
    """

    username: str
    hashed_password: str
    roles: Set[str] = field(default_factory=set)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify user password
        """

        return pwd_context.verify(plain_password, self.hashed_password)

    def has_role(self, role_name: str) -> bool:
        """
        Check if the user has a specific role.
        """

        return role_name in self.roles

    def _validate(self) -> None:
        """
        Validates the User entity's attributes.
        """

        if not self.username or not self.username.strip():
            self.notification.add_error("Username is required.")

        if self.first_name and len(self.first_name) > 100:
            self.notification.add_error(
                "First name must be at most 100 characters long."
            )

        if self.last_name and len(self.last_name) > 100:
            self.notification.add_error(
                "Last name must be at most 100 characters long."
            )

        if self.email and self.email.strip():
            try:
                valid_email = validate_email(self.email)
                self.email = valid_email.normalized
            except EmailNotValidError as e:
                self.notification.add_error(str(e))

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """

    return pwd_context.hash(password)

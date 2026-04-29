from dataclasses import dataclass, field

from email_validator import EmailNotValidError, validate_email
from passlib.context import CryptContext

from src.core.domain import EntityValidationError
from src.core.domain.entities import TenantAwareEntity
from src.core.domain.mixins import SoftDeletableMixin, UserAuditMixin

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@dataclass(kw_only=True, eq=False)
class User(TenantAwareEntity, SoftDeletableMixin, UserAuditMixin):
    """
    Entity representing a user in the system.
    """

    username: str
    hashed_password: str
    roles: set[str] = field(default_factory=set)
    permissions: set[str] = field(default_factory=set)
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None

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

    def validate(self) -> None:
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

    def __str__(self) -> str:
        """
        Returns a string representation of the User entity.
        """

        return f"User(id={self.id}, username='{self.username}')"

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the User entity.
        """

        return f"<User {self.username} ({self.id})>"


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """

    return pwd_context.hash(password)

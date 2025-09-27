from dataclasses import dataclass

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

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify user password
        """

        return pwd_context.verify(plain_password, self.hashed_password)

    def _validate(self) -> None:
        """
        Validates the User entity's attributes.
        """

        if not self.username or not self.username.strip():
            self.notification.add_error("Username is required.")

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """

    return pwd_context.hash(password)

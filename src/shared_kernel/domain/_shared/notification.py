from dataclasses import dataclass
from typing import List


@dataclass
class Notification:
    """
    A class to represent a notification containing a list of errors.
    """

    def __init__(self) -> None:
        """
        Initializes a Notification with an empty list of errors
        """

        self._errors: List[str] = []

    def add_error(self, message: str) -> None:
        """
        Adds a new error message to the Notification.

        Args:
            message: The error message to be added.
        """

        self._errors.append(message)

    @property
    def has_errors(self) -> bool:
        """
        Checks if the Notification contains any errors.

        Returns:
            bool: True if Notification contains at least one error, False otherwise.
        """

        return bool(self._errors)

    @property
    def messages(self) -> str:
        """
        Retrieve a comma-separated string of all error messages.

        Returns:
            str: A comma-separated string of error messages.
        """

        return ",".join(self._errors)

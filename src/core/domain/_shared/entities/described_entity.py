from dataclasses import dataclass, field

from src.core.domain._shared import EntityValidationError
from src.core.domain._shared.entities import AbstractEntity


@dataclass(kw_only=True, eq=False)
class DescribedEntity(AbstractEntity):
    """
    Base class for entities with only description field and default validations
    """

    description: str

    _max_description_length: int = field(default=100, init=False, repr=False)

    def update_description(self, new_description: str) -> None:
        """
        Update the description of the entity.

        Args:
            new_description (str): The new description for the entity.
        """

        self.description = new_description
        self._validate()

    def _validate(self) -> None:
        """
        Validate the entity.
        """

        if not self.description or not self.description.strip():
            self.notification.add_error("Description must be a non-empty string.")

        if len(self.description) > self._max_description_length:
            self.notification.add_error(
                f"Description must be at most {self._max_description_length} characters long."
            )

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

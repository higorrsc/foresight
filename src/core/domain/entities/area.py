from dataclasses import dataclass

from src.core.domain._shared import AbstractEntity


@dataclass(kw_only=True, eq=False)
class Area(AbstractEntity):
    """
    Entity representing a geographical or logical area within the system.
    """

    description: str

    def update_area(self, new_description: str) -> None:
        """
        Updates the description of the Area entity.
        """

        self.description = new_description
        self._validate()

    def _validate(self) -> None:
        """
        Validates the Area entity's attributes.
        """

        if not self.description or not self.description.strip():
            raise ValueError("Description must be a non-empty string.")

        if len(self.description) > 100:
            raise ValueError("Description must be at most 100 characters long.")

    def __str__(self) -> str:
        """
        Returns a string representation of the Area entity.
        """

        return f"Area(id={self.id}, description='{self.description}')"

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the Area entity.
        """

        return f"<Area {self.description} ({self.id})>"

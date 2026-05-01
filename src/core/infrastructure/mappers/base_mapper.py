from typing import Any


class BaseMapper:
    """
    Provides common mapping functionalities for auditing and soft-delete fields.
    """

    COMMON_FIELDS_TO_MAP = [
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
        "is_active",
        "deleted_at",
    ]

    @classmethod
    def map_auditing_fields_to_model(cls, entity: Any, model: Any) -> None:
        """
        Maps auditing and soft-delete fields from an entity to a model.
        """

        for field in cls.COMMON_FIELDS_TO_MAP:
            if hasattr(entity, field):
                setattr(model, field, getattr(entity, field))

    @classmethod
    def map_auditing_fields_to_entity(cls, model: Any, entity: Any) -> None:
        """
        Maps auditing and soft-delete fields from a model to an entity.
        """

        for field in cls.COMMON_FIELDS_TO_MAP:
            if hasattr(model, field) and hasattr(entity, field):
                setattr(entity, field, getattr(model, field))

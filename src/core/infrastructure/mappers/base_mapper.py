from typing import Any


class BaseMapper:
    """
    Provides common mapping functionalities for auditing and soft-delete fields.
    """

    @staticmethod
    def map_auditing_fields_to_model(entity: Any, model: Any) -> None:
        """
        Maps auditing and soft-delete fields from an entity to a model.

        This method checks for the existence of 'created_by', 'updated_by',
        and 'deleted_at' on the entity and assigns them to the model if present.
        """
        if hasattr(entity, "created_by"):
            model.created_by = entity.created_by

        if hasattr(entity, "updated_by"):
            model.updated_by = entity.updated_by

        if hasattr(entity, "deleted_at"):
            model.deleted_at = entity.deleted_at

    @staticmethod
    def map_auditing_fields_to_entity(model: Any, entity: Any) -> None:
        """
        Maps auditing and soft-delete fields from a model to an entity.

        This method uses setattr to safely assign 'created_by', 'updated_by',
        and 'deleted_at' from the model to the entity if the attributes exist on both.
        """
        for attr in ["created_by", "updated_by", "deleted_at"]:
            if hasattr(model, attr) and hasattr(entity, attr):
                setattr(entity, attr, getattr(model, attr))

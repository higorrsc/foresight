from src.shared_kernel.domain.entities.organizational_unit import OrganizationalUnit
from src.shared_kernel.infrastructure.models.organizational_unit_model import (
    OrganizationalUnitModel,
)


class OrganizationalUnitMapper:
    """
    Mapper class to convert between OrganizationalUnit entity and OrganizationalUnitModel
    """

    @staticmethod
    def to_model(entity: OrganizationalUnit) -> OrganizationalUnitModel:
        """
        Convert an OrganizationalUnit entity to an OrganizationalModel instance
        """

        model = OrganizationalUnitModel(
            id=entity.id,
            tenant_id=entity.tenant_id,
            code=entity.code,
            description=entity.description,
            parent_id=entity.parent_id,
            is_active=entity.is_active,
            created_by=entity.created_by,
            created_at=entity.created_at,
            updated_by=entity.updated_by,
            updated_at=entity.updated_at,
        )

        if hasattr(entity, "deleted_at"):
            model.deleted_at = entity.deleted_at  # type: ignore

        return model

    @staticmethod
    def to_entity(model: OrganizationalUnitModel) -> OrganizationalUnit:
        """
        Converts an OrganizationalUnitModel instance to an OrganizationalUnit
        """

        entity = OrganizationalUnit(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            code=model.code,  # type: ignore
            description=model.description,  # type: ignore
            parent_id=model.parent_id,  # type: ignore
            is_active=model.is_active,  # type: ignore
            created_by=model.created_by,  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_by=model.updated_by,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

        if hasattr(model, "deleted_at") and hasattr(entity, "deleted_at"):
            setattr(entity, "deleted_at", model.deleted_at)

        return entity

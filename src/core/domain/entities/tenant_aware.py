from dataclasses import dataclass, field
from uuid import UUID

from .entity import AbstractEntity


@dataclass(kw_only=True, eq=False, repr=False)
class TenantAwareEntity(AbstractEntity):
    """
    Base class to entities that must have a Tenant
    """

    tenant_id: UUID | None = field(default=None)

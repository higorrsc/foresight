from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from .entity import AbstractEntity


@dataclass(kw_only=True, eq=False)
class TenantAwareEntity(AbstractEntity):
    """
    Base class to entities that must have a Tenant
    """

    tenant_id: Optional[UUID] = field(default=None)

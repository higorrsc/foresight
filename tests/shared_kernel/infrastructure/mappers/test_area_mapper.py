from datetime import datetime
from uuid import uuid4

from src.shared_kernel.domain.entities import Area
from src.shared_kernel.infrastructure.mappers.area_mapper import AreaMapper
from src.shared_kernel.infrastructure.models import AreaModel


def test_area_to_model():
    tenant_id = uuid4()
    entity_id = uuid4()
    created_by = uuid4()
    created_at = datetime.now()

    entity = Area(
        id=entity_id,
        tenant_id=tenant_id,
        description="Test Area",
    )
    # Add auditing fields
    entity.created_at = created_at
    entity.created_by = created_by

    model = AreaMapper.to_model(entity)

    assert model.id == entity_id
    assert model.tenant_id == tenant_id
    assert model.description == "Test Area"
    assert model.created_at == created_at
    assert model.created_by == created_by


def test_area_to_entity():
    tenant_id = uuid4()
    model_id = uuid4()
    created_by = uuid4()
    created_at = datetime.now()

    model = AreaModel(
        id=model_id,
        tenant_id=tenant_id,
        description="Test Area Model",
        created_by=created_by,
        created_at=created_at,
    )

    entity = AreaMapper.to_entity(model)

    assert entity.id == model_id
    assert entity.tenant_id == tenant_id
    assert entity.description == "Test Area Model"
    assert entity.created_by == created_by
    assert entity.created_at == created_at

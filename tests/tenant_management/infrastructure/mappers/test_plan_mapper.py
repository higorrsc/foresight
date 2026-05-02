from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from src.tenant_management.domain.entities import Plan
from src.tenant_management.infrastructure.mappers.plan_mapper import PlanMapper
from src.tenant_management.infrastructure.models import PlanModel


def test_plan_mapper_to_model():
    plan_id = uuid4()
    entity = Plan(
        id=plan_id,
        name="Premium Plan",
        price=Decimal("99.99"),
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        created_by=uuid4(),
        updated_by=uuid4(),
    )

    model = PlanMapper.to_model(entity)

    assert model.id == plan_id
    assert model.name == "Premium Plan"
    assert model.price == Decimal("99.99")
    assert model.created_at == entity.created_at
    assert model.updated_at == entity.updated_at
    assert model.created_by == entity.created_by
    assert model.updated_by == entity.updated_by


def test_plan_mapper_to_entity():
    plan_id = uuid4()
    model = PlanModel(
        id=plan_id,
        name="Standard Plan",
        price=Decimal("49.99"),
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        created_by=uuid4(),
        updated_by=uuid4(),
    )

    entity = PlanMapper.to_entity(model)

    assert entity.id == plan_id
    assert entity.name == "Standard Plan"
    assert entity.price == Decimal("49.99")
    assert entity.created_at == model.created_at
    assert entity.updated_at == model.updated_at
    assert entity.created_by == model.created_by
    assert entity.updated_by == model.updated_by

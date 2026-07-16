from decimal import Decimal
from typing import Any
from uuid import uuid4

import pytest

from src.core.domain.exceptions import EntityValidationError
from src.tenant_management.domain.entities.plan import Plan


class TestPlan:
    """
    Test suite for the Plan entity.
    """

    def test_create_plan_with_valid_data(self) -> None:
        """
        Should create a Plan instance successfully when provided with valid data.
        """

        plan_id = uuid4()
        name = "Premium Plan"
        price = Decimal("199.99")

        plan = Plan(id=plan_id, name=name, price=price)
        plan.validate()

        assert plan.id == plan_id
        assert plan.name == name
        assert plan.price == price

    @pytest.mark.parametrize(
        "name, expected_error",
        [
            (None, "Plan name is required."),
            ("", "Plan name is required."),
            ("   ", "Plan name is required."),
            ("a" * 101, "Plan must be at most 100 characters long."),
        ],
    )
    def test_create_plan_with_invalid_name_raises_error(
        self,
        name: str | None,
        expected_error: str,
    ) -> None:
        """
        Should raise EntityValidationError for invalid names.
        """

        with pytest.raises(EntityValidationError, match=expected_error):
            Plan(name=name, price=Decimal("50.00"))  # type: ignore

    @pytest.mark.parametrize(
        "price, expected_error",
        [
            (None, "Plan price must be a valid Decimal."),
            ("not-a-decimal", "Plan price must be a valid Decimal."),
            (Decimal("0"), "Plan price must be greater than zero."),
            (Decimal("-99.9"), "Plan price must be greater than zero."),
        ],
    )
    def test_create_plan_with_invalid_price_raises_error(
        self,
        price: Any,
        expected_error: str,
    ) -> None:
        """
        Should raise EntityValidationError for invalid prices.
        """

        with pytest.raises(EntityValidationError, match=expected_error):
            Plan(name="Standard Plan", price=price)

    def test_create_plan_with_multiple_validation_errors(self) -> None:
        """
        Should raise EntityValidationError with all applicable error messages.
        """
        invalid_name = "a" * 101
        invalid_price = Decimal("-1")

        with pytest.raises(
            EntityValidationError,
            match=(
                "Plan must be at most 100 characters long.,"
                "Plan price must be greater than zero."
            ),
        ):
            Plan(name=invalid_name, price=invalid_price)

    def test_plan_string_representation(self) -> None:
        """
        Should return the correct string representation for the Plan entity.
        """

        plan_id = uuid4()
        plan = Plan(id=plan_id, name="Test Plan", price=Decimal("1.00"))

        assert str(plan) == f"Plan (id={plan.id}, name='{plan.name}')"

    def test_plan_detailed_representation(self) -> None:
        """
        Should return the correct detailed string representation for the Plan entity.
        """

        plan_id = uuid4()
        plan = Plan(id=plan_id, name="Test Plan", price=Decimal("1.00"))

        assert repr(plan) == f"<Plan id={plan.id}>"

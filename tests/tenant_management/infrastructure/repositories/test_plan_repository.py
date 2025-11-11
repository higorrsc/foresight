from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from src.tenant_management.domain.entities.plan import Plan
from src.tenant_management.infrastructure.mappers.plan_mapper import PlanMapper
from src.tenant_management.infrastructure.models.plan_model import PlanModel
from src.tenant_management.infrastructure.repositories.plan_repository import (
    PlanRepository,
)


class TestPlanRepository:
    """
    Test suite for the PlanRepository.
    """

    def test_get_by_name_found(self) -> None:
        """
        Should return a Plan entity when a plan with the given name exists.
        """

        mock_session = Mock(spec=Session)
        mock_plan_model = Mock(spec=PlanModel)
        mock_plan_entity = Mock(spec=Plan)

        with patch(
            "src.tenant_management.infrastructure.repositories.plan_repository.select"
        ) as mock_select:
            mock_session.scalars.return_value.first.return_value = mock_plan_model

            with patch.object(
                PlanMapper,
                "to_entity",
                return_value=mock_plan_entity,
            ) as mock_to_entity:
                repository = PlanRepository(session=mock_session)
                plan_name = "existing_plan"

                result = repository.get_by_name(plan_name)

                mock_select.assert_called_once_with(PlanModel)
                mock_session.scalars.assert_called_once()
                mock_to_entity.assert_called_once_with(mock_plan_model)
                assert result == mock_plan_entity

    def test_get_by_name_not_found(self) -> None:
        """
        Should return None when no plan with the given name exists.
        """

        mock_session = Mock(spec=Session)
        mock_session.scalars.return_value.first.return_value = None

        with patch(
            "src.tenant_management.infrastructure.repositories.plan_repository.select"
        ):
            with patch.object(PlanMapper, "to_entity") as mock_to_entity:
                repository = PlanRepository(session=mock_session)
                plan_name = "non_existing_plan"

                result = repository.get_by_name(plan_name)

                assert result is None
                mock_to_entity.assert_not_called()

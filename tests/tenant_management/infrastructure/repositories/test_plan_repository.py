from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.tenant_management.domain.entities import Plan
from src.tenant_management.infrastructure.mappers import PlanMapper
from src.tenant_management.infrastructure.models import PlanModel
from src.tenant_management.infrastructure.repositories import PlanRepository


class TestPlanRepository:
    """
    Test suite for the PlanRepository.
    """

    async def test_get_by_name_found(self) -> None:
        """
        Should return a Plan entity when a plan with the given name exists.
        """

        mock_session = AsyncMock(spec=AsyncSession)

        mock_plan_model = MagicMock(spec=PlanModel)
        mock_plan_entity = MagicMock(spec=Plan)

        mock_result = MagicMock()
        mock_result.unique.return_value.scalar_one_or_none.return_value = (
            mock_plan_model
        )

        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.tenant_management.infrastructure.repositories.plan_repository.select"
        ) as mock_select:
            with patch.object(
                PlanMapper,
                "to_entity",
                return_value=mock_plan_entity,
            ) as mock_to_entity:
                repository = PlanRepository(session=mock_session)
                plan_name = "existing_plan"

                result = await repository.get_by_name(plan_name)

                mock_select.assert_called_once_with(PlanModel)
                mock_session.execute.assert_called_once()
                mock_to_entity.assert_called_once_with(mock_plan_model)
                assert result == mock_plan_entity

    async def test_get_by_name_not_found(self) -> None:
        """
        Should return None when no plan with the given name exists.
        """

        mock_session = AsyncMock(spec=AsyncSession)

        mock_result = MagicMock()
        mock_result.unique.return_value.scalar_one_or_none.return_value = None

        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.tenant_management.infrastructure.repositories.plan_repository.select"
        ):
            with patch.object(PlanMapper, "to_entity") as mock_to_entity:
                repository = PlanRepository(session=mock_session)
                plan_name = "non_existing_plan"

                result = await repository.get_by_name(plan_name)

                assert result is None
                mock_to_entity.assert_not_called()

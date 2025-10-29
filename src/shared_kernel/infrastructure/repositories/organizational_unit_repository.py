from sqlalchemy.orm import Session

from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.infrastructure.mappers import OrganizationalUnitMapper
from src.shared_kernel.infrastructure.models import OrganizationalUnitModel
from src.shared_kernel.infrastructure.repositories._shared import SQLAlchemyRepository


class OrganizationalUnitRepository(
    SQLAlchemyRepository[OrganizationalUnit, OrganizationalUnitModel]
):
    """
    Repository for manning OrganizationalUnit entities using SQLAlchemy

    :param session: SQLAlchemy session.
    """

    def __init__(self, session: Session):
        """
        Initialize the OrganizationalUnitRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(
            session,
            OrganizationalUnitModel,
            mapper=OrganizationalUnitMapper,
        )

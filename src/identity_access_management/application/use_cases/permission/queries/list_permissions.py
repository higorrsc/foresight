from math import ceil

from src.core.application import PaginatedResponseDTO
from src.core.application.dto import PaginationMeta
from src.core.application.use_cases.queries import ListRequestInputDTO
from src.identity_access_management.domain.entities import Permission
from src.identity_access_management.domain.repositories import IPermissionRepository


class ListPermissionsUseCase:
    """
    Use case to list all available system permissions.
    Usually restricted do Admins or users who can manage roles.
    """

    def __init__(self, repository: IPermissionRepository):
        """
        Initialize the use case.

        :param repository: The repository to use for listing permissions.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: ListRequestInputDTO,
    ) -> PaginatedResponseDTO[Permission]:
        """
        Execute the use case.

        :param input_dto: The input DTO for the use case.
        :return: A list of permissions.
        """

        all_permissions = self._repository.list_all()

        # Ordena a lista de permissões pelo atributo 'code'
        sorted_permissions = sorted(all_permissions, key=lambda p: p.codename)

        total_items = len(sorted_permissions)
        start = input_dto.offset
        end = start + input_dto.limit
        paginated_data = sorted_permissions[start:end]

        page_size = input_dto.limit
        if page_size > 0:
            total_pages = ceil(total_items / page_size)
            current_page = start // page_size + 1
        else:
            total_pages = 0
            current_page = 1

        return PaginatedResponseDTO(
            data=paginated_data,
            meta=PaginationMeta(
                total_items=total_items,
                current_page=current_page,
                page_size=page_size,
                total_pages=total_pages,
            ),
        )

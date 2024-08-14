from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from src.auth.dependencies import get_current_active_auth_user
from src.datasets.service import TypeDatasetService, DatasetService
from src.datasets.schemas import TypeDatasetRead, DatasetRead
from src.users.schemas import UserRead


error_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f'User not found',
)


async def get_types_depend(
    service: Annotated[TypeDatasetService, Depends()]
) -> list[TypeDatasetRead]:
    types = await service.get_types()
    return list(types)


async def valid_type_id(type_id: int, service: TypeDatasetService) -> TypeDatasetRead:
    type = await service.get_type_by_id(type_id)

    if not type:
        raise error_found

    return type


async def valid_dataset_id(
    dataset_id: Annotated[int, Path], service: Annotated[DatasetService, Depends()]
) -> DatasetRead:
    dataset = await service.get_dataset_by_id(dataset_id)

    if not dataset:
        raise error_found

    return dataset


async def get_dataset_for_sale_depend(
    page: Annotated[int, Path(ge=1)], service: Annotated[DatasetService, Depends()]
) -> list[DatasetRead]:
    dataset = await service.get_dataset_for_sale(page)
    return list(dataset)


async def get_count_dataset_for_sale_depend(
    service: Annotated[DatasetService, Depends()]
) -> int:
    total_count = await service.get_count_dataset_for_sale()
    return total_count


async def get_dataset_by_user_id_depend(
    user_id: int, service: DatasetService
) -> list[DatasetRead]:
    dataset = await service.get_dataset_by_user_id(user_id)
    return list(dataset)


async def get_dataset_by_id_and_user_for_delete(
    dataset_id: Annotated[int, Path],
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    service: Annotated[DatasetService, Depends()],
):
    if user.is_superuser:
        st = await service.delete_dataset_by_id(dataset_id)
        return st
    return f'This {user.username} is not super user {user.is_superuser=}'

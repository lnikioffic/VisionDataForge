from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from src.datasets.service import TypeDatasetService
from src.datasets.schemas import TypeDatasetRead


error_found = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )


async def get_types_depend(service: Annotated[TypeDatasetService, Depends()]) -> list[TypeDatasetRead]:
    types = await service.get_types()
    return list(types)


async def valid_type_id(
    type_id: Annotated[int, Path], 
    service: Annotated[TypeDatasetService, Depends()]
) -> TypeDatasetRead | None:
    type = await service.get_type_by_id(type_id)
    
    if not type:
        raise error_found
        
    return type
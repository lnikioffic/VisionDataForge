from typing import Annotated
from fastapi import Depends, HTTPException, Path, status

from src.users.schemas import UserLogin, UserRead
from src.users.service import UserService


error_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f'User not found',
)


async def valid_user_username(user_name: str, service: UserService) -> UserLogin:
    user = await service.get_user_by_username(user_name)

    if not user:
        raise error_found

    return user


async def valid_user_id(
    user_id: Annotated[int, Path], service: UserService
) -> UserRead | None:
    user = await service.get_user_by_id(user_id)

    if not user:
        raise error_found

    return user

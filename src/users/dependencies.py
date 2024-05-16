from fastapi import Depends, HTTPException, status

from src.users.schemas import UserLogin, UserRead
from src.users.service import ServiceUser


error_found = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )


async def valid_user_username(user_name: str, service: ServiceUser) -> UserLogin:
    user = await service.get_user_by_username(user_name)
    
    if not user:
        raise error_found
        
    return user


async def valid_user_id(user_id: int, service: ServiceUser) -> UserRead | None:
    user = await service.get_user_by_id(user_id)
    
    if not user:
        raise error_found
        
    return user
 
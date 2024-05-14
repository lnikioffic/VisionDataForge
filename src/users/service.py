from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from fastapi import Depends, HTTPException, status

from src.users.schemas import UserLogin, UserRead, UserCreate
from src.users.models import User
from src.auth import utils as auth_utils
from src.database import db


class ServiceUser():
    def __init__(self, session: AsyncSession = Depends(db.get_session)) -> None:
        self.session = session
        
        
    async def get_user_by_username(self, username: str) -> UserLogin:
        stmt = select(User).filter(User.username == username)
        result: Result = await self.session.execute(stmt)
        user = result.scalar()
        return user
    

    async def get_user_by_id(self, id: int) -> UserRead | None:
        user = await self.session.get(User, id)
        return user
    
    
    async def create_user(self, user: UserCreate) -> UserRead:
        stmt = select(User).filter(User.email == user.email)
        result = await self.session.execute(stmt)
        user_exists = result.scalars().all()
        if len(user_exists) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exist"
            )
        user.hashed_password = auth_utils.hash_password(user.hashed_password).decode()
        add_user = User(**user.model_dump())
        self.session.add(add_user)
        await self.session.commit()
        return add_user
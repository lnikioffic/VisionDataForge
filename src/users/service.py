from sqlalchemy.engine import Result
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from pydantic import EmailStr

from src.users.schemas import (
    UserLogin,
    UserRead,
    UserCreate,
    UserUpdate,
    UserUpdatePartial,
)
from src.users.models import User
from src.auth import utils as auth_utils
from src.service import Service


class UserService(Service):
    async def get_user_by_username(self, username: str) -> UserLogin | None:
        stmt = select(User).filter(User.username == username)
        result: Result = await self.session.execute(stmt)
        user = result.scalar()
        return user

    async def get_user_by_id(self, id: int) -> User | None:
        user = await self.session.get(User, id)
        return user

    async def get_user_by_email(self, email: EmailStr) -> UserLogin | None:
        stmt = select(User).filter(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar()
        return user

    async def create_user(self, user: UserCreate) -> UserRead:

        email_exist = await self.get_user_by_email(user.email)
        username_exist = await self.get_user_by_username(user.username)

        if email_exist is not None or username_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User with this email or username already exist',
            )

        user.hashed_password = auth_utils.hash_password(user.hashed_password).decode()
        add_user = User(**user.model_dump())
        self.session.add(add_user)
        await self.session.commit()
        return add_user

    async def update_user(
        self,
        user: UserRead,
        user_update: UserUpdate | UserUpdatePartial,
        partial: bool = False,
    ) -> UserRead:
        user_data = user_update.model_dump(exclude_unset=partial)
        if user_data['hashed_password'] != None:
            user_data['hashed_password'] = auth_utils.hash_password(
                user_data['hashed_password']
            ).decode()
        for key, value in user_data.items():
            if value != None:
                setattr(user, key, value)
        await self.session.commit()
        return user  

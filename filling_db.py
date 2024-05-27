from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
import asyncio

from src.database import db
from src.auth import utils as auth_utils
from src.videoprocessor.schemas import TypeAnnotation
from src.datasets.schemas import TypeDatasetCreate, TypeDatasetRead
from src.users.schemas import UserCreateSuperuser, UserLogin, UserRead
from src.users.models import User
from src.datasets.models import TypeDataset



async def get_user_by_username(username: str, session: AsyncSession) -> UserLogin | None:
    stmt = select(User).filter(User.username == username)
    result: Result = await session.execute(stmt)
    user = result.scalar()
    return user
    
    
async def get_user_by_email(email: EmailStr, session: AsyncSession) -> UserLogin | None:
    stmt = select(User).filter(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar()
    return user


async def create_user(user: UserCreateSuperuser, session: AsyncSession) -> UserRead:

        email_exist = await get_user_by_email(user.email, session)
        username_exist = await get_user_by_username(user.username, session)
        
        if email_exist is not None or username_exist is not None:
            print(f'такой пользователь есть: {user.username}')
            return
            
        user.hashed_password = auth_utils.hash_password(user.hashed_password).decode()
        add_user = User(**user.model_dump())
        session.add(add_user)
        await session.commit()
        return add_user
    

async def get_types(session: AsyncSession) -> list[TypeDatasetRead]:
    stmt = select(TypeDataset)
    result: Result = await session.execute(stmt)
    types = result.scalars().all()
    return types
       

async def get_type_by_name(name: str, session: AsyncSession) -> TypeDatasetRead | None:
    stmt = select(TypeDataset).filter(TypeDataset.name == name)
    result: Result = await session.execute(stmt)
    type_data = result.scalar()
    return type_data


async def create_types(names: list[TypeDatasetCreate], session: AsyncSession):
    model_names_types = [TypeDataset(**name.model_dump()) for name in names]
    session.add_all(model_names_types)
    await session.commit()
    print(model_names_types)
    
       
async def main(user):
    async with db.async_session() as session:
        await create_user(user, session)
        
        enum_names_types = [typ.name for typ in TypeAnnotation]
        database_names_types = await get_types(session) 
        
        enum_names_types_copy =enum_names_types.copy()
        is_in_type = False
        
        for name in database_names_types:
                if name.name not in enum_names_types:
                    is_in_type = True
                    print(f'нету этого типа в Enum: {name.name}')
                if name.name in enum_names_types_copy:
                    enum_names_types_copy.remove(name.name)
                    
        if len(database_names_types) == len(enum_names_types) or is_in_type:
            print('обновление не требуется')
            return

        types = [TypeDatasetCreate(name=name) for name in enum_names_types]
        await create_types(types, session)
                
    
if __name__ == '__main__':
    user = UserCreateSuperuser(
        username='admin',
        email='email@email.ru',
        hashed_password='admin',
        is_superuser=True
    )

    asyncio.run(main(user))

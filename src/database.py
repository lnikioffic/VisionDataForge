from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker, 
    AsyncSession)
from typing import AsyncGenerator

from src.config import settings


class DataBase:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)


    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            yield session


db = DataBase(url=settings.db_url)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from pydantic import EmailStr

from src.videoprocessor.models import UserDataset
from src.videoprocessor.schemas import DatasetCreate, DatasetRead
from src.users.schemas import UserRead
from src.database import db


class DataStorageService():
    def __init__(self, session: AsyncSession = Depends(db.get_session)) -> None:
        self.session = session
        
        
    async def create_dataset(self, dataset: DatasetCreate) -> DatasetRead:
        add_dataset = UserDataset(**dataset.model_dump())
        self.session.add(add_dataset)
        await self.session.commit()
        return add_dataset
        
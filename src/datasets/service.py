from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from fastapi import Depends

from src.datasets.models import TypeDataset
from src.datasets.schemas import TypeDatasetRead
from src.database import db


class TypeDatasetService():
    def __init__(self, session: AsyncSession = Depends(db.get_session)) -> None:
        self.session = session
        
        
    async def get_type_by_id(self, id) -> TypeDatasetRead | None:
        type = await self.session.get(TypeDataset, id)
        return type
    
    
    async def get_types(self) -> list[TypeDatasetRead]:
        stmt = select(TypeDataset)
        result: Result = await self.session.execute(stmt)
        types = result.scalars().all()
        return types
        
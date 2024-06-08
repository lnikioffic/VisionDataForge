from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.database import db


class Service:
    def __init__(self, session: AsyncSession = Depends(db.get_session)) -> None:
        self.session = session

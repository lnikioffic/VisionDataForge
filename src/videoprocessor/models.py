from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.users.models import User

"""
Дата сеты пользователей, связаны с пользователем
"""
class UserDataset(Base):
    __tablename__ = 'user_dataset'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    format: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100))
    file_path: Mapped[str] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(
        back_populates='datasets'
    )
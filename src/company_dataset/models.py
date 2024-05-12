from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.order.models import Order

"""
Дата сеты компании
"""
class CompanyDataset(Base):

    __tablename__ = 'company_dataset'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    format: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(default=1, server_default='1')
    description: Mapped[str] = mapped_column(String(100))
    file_path: Mapped[str] = mapped_column(String(100))

    orders: Mapped[list['Order']] = relationship (
        secondary='company_dataset_order',
        back_populates='companys_datasets'
    )
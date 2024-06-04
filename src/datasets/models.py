from typing import TYPE_CHECKING
from datetime import datetime  

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.order.models import DatasetOrder
    from src.users.models import User

"""
Дата сеты
"""
class Dataset(Base):

    __tablename__ = 'dataset'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int | None]
    
    count_frames: Mapped[int]
    count_classes: Mapped[int]
    
    file_path: Mapped[str] = mapped_column(String(100))
    first_frame: Mapped[str] = mapped_column(String(100))
    second_frame: Mapped[str] = mapped_column(String(100))
    size: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    for_sale: Mapped[bool] = mapped_column(server_default='false', default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', onupdate='CASCADE', ondelete='RESTRICT'))
    
    type_dataset_id: Mapped[int] = mapped_column(ForeignKey('type_dataset.id', onupdate='CASCADE', ondelete='RESTRICT'))

    type_dataset: Mapped['TypeDataset'] = relationship(
        back_populates='datasets_for_type'
    )
    
    # orders: Mapped[list['Order']] = relationship (
    #     secondary='company_dataset_order',
    #     back_populates='companys_datasets'
    # )
    user: Mapped['User'] = relationship(
        back_populates='datasets'
    )
 
    orders_details: Mapped[list['DatasetOrder']] = relationship(
        back_populates='dataset'
    )


class TypeDataset(Base):
    __tablename__ = 'type_dataset'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    
    datasets_for_type: Mapped[list['Dataset']] = relationship(back_populates='type_dataset')
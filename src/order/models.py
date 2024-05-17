from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.datasets.models import Dataset

if TYPE_CHECKING:
    from src.users.models import User


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[int | None]
    payment: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', onupdate='CASCADE', ondelete='RESTRICT'))

    user: Mapped['User'] = relationship(
        back_populates='orders_user'
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )

    # companys_datasets: Mapped[list['CompanyDataset']] = relationship(
    #     secondary='company_dataset_order',
    #     back_populates='orders'
    # )
    
    # связь через ассоциативную модель
    dataset_details: Mapped[list['DatasetOrder']] = relationship(
        back_populates='order'
    )


class DatasetOrder(Base):
    __tablename__ = 'dataset_order'
    __table_args__ = (UniqueConstraint('order_id', 'dataset_id', name='idx_unique'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id', onupdate='CASCADE', ondelete='CASCADE'))
    dataset_id: Mapped[int] = mapped_column(ForeignKey('dataset.id', onupdate='CASCADE', ondelete='RESTRICT'))
    
    # association between Assocation -> Order
    order: Mapped['Order'] = relationship(
        back_populates='dataset_details',
    )

    # association between Assocation -> Product
    dataset: Mapped['Dataset'] = relationship(
        back_populates='orders_details',
    )
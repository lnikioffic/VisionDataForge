from sqlalchemy.engine import Result
from sqlalchemy import func, select, delete
from sqlalchemy.orm import joinedload, selectinload

from src.datasets.models import Dataset
from src.order.models import Order, DatasetOrder
from src.order.schemas import OrderCreate, OrderRead
from src.service import Service


class OrderService(Service):
    async def get_orders(self) -> list[OrderRead]:
        stmt = select(Order).options(
            joinedload(Order.datasets_details).options(
                selectinload(DatasetOrder.dataset).options(
                    selectinload(Dataset.user), selectinload(Dataset.type_dataset)
                )
            ),
            selectinload(Order.user),
        )
        result: Result = await self.session.execute(stmt)
        orders = result.unique().scalars().all()
        return list(orders)

    async def create_order(
        self, order: OrderCreate, user_id: int, datasets_ids: list[int]
    ):
        try:
            order = Order(**order.model_dump(), user_id=user_id)
            for dataset_id in datasets_ids:
                order.datasets_details.append(DatasetOrder(dataset_id=dataset_id))

            self.session.add_all(
                [
                    order,
                ]
            )
            await self.session.commit()
        except Exception as ex:
            await self.session.rollback()
            return f'excption {ex}'

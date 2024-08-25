from pydantic import BaseModel, ConfigDict

from src.datasets.schemas import DatasetRead
from src.users.schemas import UserRead


class DatasetOrderBase(BaseModel):
    dataset: DatasetRead


class DatasetOrderRead(DatasetOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class DatasetOrderCreate(BaseModel):
    order_id: int
    dataset_id: int


class DatasetOrderUpdate(DatasetOrderCreate):
    pass


class OrderBase(BaseModel):
    total_price: int | None
    payment: bool = False


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserRead
    datasets_details: list[DatasetOrderRead]

class OrderCreate(OrderBase):
    pass

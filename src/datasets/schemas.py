from pydantic import BaseModel, ConfigDict

from src.users.schemas import UserRead


class TypeDatasetBase(BaseModel):
    name: str


class TypeDatasetRead(TypeDatasetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TypeDatasetCreate(TypeDatasetBase):
    pass


class TypeDatasetUpdate(TypeDatasetBase):
    pass


class DatasetBase(BaseModel):
    name: str
    price: int | None

    count_frames: int
    count_classes: int

    file_path: str
    first_frame: str
    second_frame: str

    size: str

    for_sale: bool = False


class DatasetCreate(DatasetBase):
    pass


class DatasetRead(DatasetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserRead
    type_dataset: TypeDatasetRead


class DabaseUpdate(DatasetBase):
    name: str | None = None
    description: str | None = None
    file_path: str | None = None
    first_frame: str | None = None
    second_frame: str | None = None

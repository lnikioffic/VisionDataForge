from pydantic import BaseModel, ConfigDict, Field

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
    description: str
    file_path: str
    first_frame: str
    second_frame: str


class DatasetCreate(DatasetBase):
    user: UserRead
    
    
class DatasetRead(DatasetCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    
    
class DabaseUpdate(DatasetBase):
    name: str | None = None
    description: str | None = None
    file_path: str | None = None
    first_frame: str | None = None
    second_frame: str | None = None
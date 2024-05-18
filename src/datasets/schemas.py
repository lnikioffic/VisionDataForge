from pydantic import BaseModel, ConfigDict, Field


class TypeDatasetBase(BaseModel):
    name: str


class TypeDatasetRead(TypeDatasetBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    
    
class TypeDatasetCreate(TypeDatasetBase):
    pass


class TypeDatasetUpdate(TypeDatasetBase):
    pass
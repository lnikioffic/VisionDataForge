from pydantic import BaseModel, ConfigDict, Field
import enum

from src.users.schemas import UserRead

class BoundingBoxesObject(BaseModel):
    name_class: str = Field(examples=['Каска'])
    bboxes: list[list[int]] = Field(examples=[[[597, 142, 60, 32], [5, 165, 40, 36]]])


class FrameData(BaseModel):
    current_frame: int
    names_class: list[str] = Field(examples=[['Каска']])
    frame_width: int
    frame_height: int
    bboxes_objects: list[BoundingBoxesObject]
    
    
class TypeAnnotation(enum.Enum):
    yolo_dark = 'yolo_dark'
    
    
class FormData(BaseModel):
    type_annotation: TypeAnnotation = Field(examples=[TypeAnnotation.yolo_dark])
    frame_data: FrameData
    
    
class DatasetBase(BaseModel):
    name: str
    format: str
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
    format: str | None = None
    description: str | None = None
    file_path: str | None = None
    first_frame: str | None = None
    second_frame: str | None = None
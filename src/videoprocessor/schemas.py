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
    
    
@enum.unique
class TypeAnnotation(enum.Enum):
    yolo_dark: str = 'yolo_dark'
    
    
class FormData(BaseModel):
    type_annotation: TypeAnnotation = Field(examples=[TypeAnnotation.yolo_dark])
    frame_data: FrameData


class MetaDataVideo(BaseModel):
    fps: int
    count_frames: int
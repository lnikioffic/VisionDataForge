import numpy as np
from pydantic import BaseModel, ConfigDict, Field
import enum
from dataclasses import dataclass

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
    type_annotation_id: int
    frame_data: FrameData


class MetaDataVideo(BaseModel):
    fps: int
    count_frames: int
    

@dataclass
class ROIsObject:
    name_class: str
    ROIs: list[list[int]]
    

@dataclass
class Frame:
    frame: np.array
    names_classes: list[ROIsObject]
from pydantic import BaseModel, Field


class BoundingBoxesObject(BaseModel):
    name_class: str = Field(examples=['Каска'])
    bboxes: list[list[int]] = Field(examples=[[[597, 142, 60, 32], [5, 165, 40, 36]]])


class FrameData(BaseModel):
    current_frame: int
    names_class: list[str] = Field(examples=[['Каска']])
    frame_width: int
    frame_hight: int
    bboxes_objects: list[BoundingBoxesObject]
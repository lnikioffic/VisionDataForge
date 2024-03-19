from pydantic import BaseModel, Field


class BoundingBoxesObject(BaseModel):
    name_class: str = Field(examples=['Каска'])
    bboxes: list[list[int]] = Field(examples=[[[597, 142, 60, 32], [5, 165, 40, 36]]])


class FrameData(BaseModel):
    names_class: list[str] = Field(examples=[['Каска']])
    bboxes_objects: list[BoundingBoxesObject]
    current_frame: int
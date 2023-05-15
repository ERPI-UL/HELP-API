from pydantic import BaseModel


class Position(BaseModel):
    """ Position pydantic model"""
    x: float
    y: float
    z: float

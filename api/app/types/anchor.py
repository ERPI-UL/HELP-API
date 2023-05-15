from app.types.position import Position
from pydantic import BaseModel


class Anchor(BaseModel):
    """ Anchor pydantic model """
    position: Position
    rotation: Position

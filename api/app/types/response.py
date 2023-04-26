from pydantic import BaseModel


class IDResponse(BaseModel):
    """ IDResponse pydantic model"""
    id: int

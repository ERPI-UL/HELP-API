from pydantic import BaseModel


class IDResponse(BaseModel):
    """ IDResponse pydantic model"""
    id: int


class OKResponse(BaseModel):
    """ OKResponse pydantic model"""
    ok: str

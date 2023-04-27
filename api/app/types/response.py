from pydantic import BaseModel


class IDResponse(BaseModel):
    """ IDResponse pydantic model, used to return an id of a created object"""
    id: int


class OKResponse(BaseModel):
    """ OKResponse pydantic model, used to indicate that the request was successful"""
    ok: str

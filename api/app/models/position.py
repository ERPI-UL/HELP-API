from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model


class Position(Model):
    """ Position model"""
    id = fields.IntField(pk=True)
    x = fields.FloatField()
    y = fields.FloatField()
    z = fields.FloatField()

    class Meta:
        """ Meta class for Position model"""
        table = "positions"


class PositionPost(BaseModel):
    """ PositionPost pydantic model"""
    x: float
    y: float
    z: float

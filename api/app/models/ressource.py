from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model

from app.models.user import ShortUserOut


class Ressource(Model):
    """ Ressource model , represent a file link to an object"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    owner = fields.ForeignKeyField('models.User', related_name='ressources')
    path = fields.CharField(max_length=255, null=True)

    class Meta:
        """ Meta class for Ressource model"""
        table = "ressources"


class RessourceOut(BaseModel):
    """ Ressource model for output"""
    id: int
    name: str
    path: str
    owner: ShortUserOut

    class Config:
        """ Config class for RessourceOut"""
        orm_mode = True

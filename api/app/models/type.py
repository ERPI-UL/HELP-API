from tortoise import fields
from tortoise.models import Model
from pydantic import BaseModel, validator


class Type(Model):
    """ Type model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    # choice = fields.ForeignKeyField('models.Choice', related_name='choice',null=True)

    class Meta:
        """ Meta class for Type model"""
        table = "types"


class TypePost(BaseModel):
    """ TypePost pydantic model"""
    name: str

    @validator('name')
    @classmethod
    def name_validator(cls, value):
        """ verify if the type is valid"""
        if value not in ['choice', 'info', 'action']:
            raise ValueError('Name must be choice, step or action')
        return value

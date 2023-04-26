from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Target(Model):
    """ Target model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    machine = fields.ForeignKeyField('models.Machine', related_name='targets')

    class Meta:
        """ Meta class for Target model"""
        table = "targets"
        unique_together = ('name', 'machine_id')


TargetOut = pydantic_model_creator(
    Target, name='TargetOut', include=['id', 'name'])


class TargetPost(BaseModel):
    """ TargetPost pydantic model"""
    name: str

from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Target(Model):
    """ Target model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    artifact = fields.ForeignKeyField('models.Artifact', related_name='targets', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for Target model"""
        table = "targets"
        unique_together = ('name', 'artifact_id')


class TargetPost(BaseModel):
    """ TargetPost pydantic model"""
    name: str


class TargetOut(BaseModel):
    """ TargetOut pydantic model"""
    id: int
    name: str
    artifact: int
    components: list[int] = []


class TargetIn(BaseModel):
    """ TargetIn pydantic model"""
    name: str
    artifact: int


class TargetInUpdate(BaseModel):
    """ TargetInUpdate pydantic model"""
    name: str = None
    artifact: int = None

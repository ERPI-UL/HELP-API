from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class MachineText(Model):
    """ MachineText model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='machineTexts')
    machine = fields.ForeignKeyField(
        'models.Machine', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for MachineText model"""
        table = "machinetext"


class Machine(Model):
    """ Machine model"""
    id = fields.IntField(pk=True)
    path = fields.TextField(null=True)
    # scenarios: fields.ReverseRelation["Scenario"]

    class Meta:
        """ Meta class for Machine model"""
        table = "machines"


class MachinePost(BaseModel):
    """ MachinePost pydantic model"""
    name: str = None
    id: int = None


Machinein = pydantic_model_creator(
    Machine, name='Machinein', exclude_readonly=True)
MachineOut = pydantic_model_creator(
    Machine, name='MachineOut')

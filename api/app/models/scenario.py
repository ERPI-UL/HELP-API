from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from app.models.machine import MachinePost
from app.models.step import StepPost


class ScenarioText(Model):
    """ ScenarioText model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='scenarioTexts')
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for ScenarioText model"""
        table = "scenariotext"


class Scenario(Model):
    """ Scenario model"""
    id = fields.IntField(pk=True)
    machine = fields.ForeignKeyField(
        'models.Machine', related_name='scenarios', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for Scenario model"""
        table = "scenarios"
        # unique_together = ('name', 'scenarios.machineName')


class ScenarioUpdate(BaseModel):
    """ ScenarioUpdate pydantic model"""
    name: str
    description: str
    idMachine: int


class ScenarioCreate(BaseModel):
    """ ScenarioCreate pydantic model"""
    name: str
    description: str
    machine: int


class ScenarioPost(BaseModel):
    """ ScenarioPost pydantic model"""
    name: str
    description: str
    machine: MachinePost
    steps: list[StepPost]


ScenarioOut = pydantic_model_creator(
    Scenario, name='ScenarioOut')

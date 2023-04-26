from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class PlayedStep(Model):
    """ playedStep model """
    id = fields.IntField(pk=True)
    step = fields.ForeignKeyField(
        'models.Step', related_name='playedSteps', on_delete=fields.CASCADE)
    session = fields.ForeignKeyField(
        'models.Session', related_name='playedSteps', on_delete=fields.CASCADE)
    progressNumber = fields.IntField(default=0)  # garantie l'ordre des steps
    missed = fields.BooleanField(default=False)
    skipped = fields.BooleanField(default=False)
    record = fields.TextField()  # json
    time = fields.IntField(default=0)

    class Meta:
        """ Meta class for playedStep model"""
        table = "playedSteps"
        ordering = ['progressNumber']


class PlayedStepPost(BaseModel):
    """ playedStepPost pydantic model"""
    progressNumber: int
    missed: bool
    skipped: bool
    record: str
    stepid: int
    time: int


playedStepIn = pydantic_model_creator(
    PlayedStep, name='playedStepIn')

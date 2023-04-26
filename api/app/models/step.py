from pydantic import BaseModel, validator
from tortoise import fields
from tortoise.models import Model

from app.models.choice import ChoicePost
from app.models.position import PositionPost
from app.models.type import TypePost


class StepText(Model):
    """ StepText model"""
    id = fields.IntField(pk=True)
    label = fields.TextField()
    description = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='stepTexts')
    step = fields.ForeignKeyField(
        'models.Step', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for StepText model"""
        table = "steptext"


class StepPost(BaseModel):
    """ StepPost pydantic model"""
    name: str
    label: str
    description: str
    ordernumber: int
    position: PositionPost
    type: TypePost
    targets: list[int] = None
    choice: ChoicePost = None

    @validator('ordernumber')
    @classmethod
    def ordernumber_validator(cls, value):
        """ verify if the ordernumber is valid"""
        if value < 0:
            raise ValueError('ordernumber must be >= 0')
        return value


class Step(Model):
    """ Step model"""
    id = fields.IntField(pk=True)
    type = fields.ForeignKeyField('models.Type', related_name='steps')
    name = fields.TextField()  # logical purpose , do not translate
    ressourcePath = fields.TextField(null=True)
    hint = fields.TextField(null=True)
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='steps', on_delete=fields.CASCADE)
    targets = fields.ManyToManyField(
        'models.Target', related_name='steps', null=True)
    position = fields.ForeignKeyField(
        'models.Position', related_name='steps', null=True, on_delete=fields.CASCADE)
    choice = fields.ForeignKeyField(
        'models.Choice', related_name='steps', null=True, on_delete=fields.RESTRICT)
    ordernumber = fields.IntField()

    class Meta:
        """ Meta class for Step model"""
        table = "steps"
        unique_together = ('scenario_id', 'ordernumber')
        ordering = ['ordernumber']

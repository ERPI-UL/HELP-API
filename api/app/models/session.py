from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Session(Model):
    """ Session model"""
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        'models.User', related_name='sessions')
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='sessions', on_delete=fields.CASCADE)
    evaluation = fields.BooleanField()
    vrmode = fields.BooleanField(null=True)
    date = fields.DatetimeField(auto_now_add=True)


class SessionIn(BaseModel):
    """ SessionIn pydantic model"""
    scenarioid: int
    date: str
    evaluation: bool
    vrmode: bool = None


SessionOut = pydantic_model_creator(
    Session, name='SessionOut', include=['id', 'date', 'evaluation', 'scenario_id', 'vrmode'])
SessioninFront = pydantic_model_creator(
    Session, name='SessioninFront', exclude_readonly=True)

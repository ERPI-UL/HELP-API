from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model


class ChoiceText(Model):
    """ ChoiceText model """
    id = fields.IntField(pk=True)
    labelleft = fields.TextField()
    labelright = fields.TextField()
    redirectleft = fields.TextField()
    redirectright = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='choiceTexts')
    choice = fields.ForeignKeyField(
        'models.Choice', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for ChoiceText model"""
        table = "choicetext"


class Choice(Model):
    """ Choice model"""
    id = fields.IntField(pk=True)
    labelleft = fields.TextField()
    labelright = fields.TextField()
    redirectleft = fields.TextField()
    redirectright = fields.TextField()

    class Meta:
        """ Meta class for Choice model"""
        table = "choices"


class ChoiceOptions(BaseModel):
    """ ChoiceOptions pydantic model"""
    label: str
    redirect: str


class ChoicePost(BaseModel):
    """ ChoicePost pydantic model"""
    option_left: ChoiceOptions
    option_right: ChoiceOptions

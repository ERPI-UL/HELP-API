from typing import Optional

from pydantic import BaseModel, StrictStr, validator
from tortoise import Model, fields

from app.models.position import PositionPost


class Action(Model):
    """ Action model """
    id = fields.IntField(pk=True)
    tag = fields.CharField(max_length=50)  # do not translate, logical purpose see the DOC
    next = fields.ForeignKeyField('models.Action', related_name='previous_set', null=True, on_delete=fields.SET_NULL)
    previous = fields.ForeignKeyField('models.Action', related_name='next_set', null=True, on_delete=fields.SET_NULL)
    type = fields.ForeignKeyField('models.Type', related_name='actions', on_delete=fields.CASCADE)
    artifact = fields.ForeignKeyField('models.Artifact', related_name='actions', null=True, on_delete=fields.CASCADE)
    targets = fields.ManyToManyField('models.Target', related_name='actions', through='action_target')
    # activity = fields.ForeignKeyField('models.Activity', related_name='actions', on_delete=fields.CASCADE)
    # choice
    left_target_action = fields.ForeignKeyField('models.Action', related_name='left_choice_set', null=True, on_delete=fields.SET_NULL)
    right_target_action = fields.ForeignKeyField('models.Action', related_name='right_choice_set', null=True, on_delete=fields.SET_NULL)

    # for garbage collector
    updated_at = fields.DatetimeField(auto_now=True)

    x = fields.FloatField()
    y = fields.FloatField()
    z = fields.FloatField()

    ressourcePath = fields.CharField(max_length=100, null=True)

    class Meta:
        """ Meta class for Action model """
        table = "action"
        # unique_together = (("tag", "activity_id"))


class ActionText(Model):
    """ ActionText model """
    id = fields.IntField(pk=True)
    name = fields.TextField(max_length=50)
    description = fields.TextField()
    hint = fields.TextField(null=True)
    language = fields.ForeignKeyField('models.Language', related_name='actionTexts')
    action = fields.ForeignKeyField('models.Action', related_name='texts', on_delete=fields.CASCADE)

    left_choice = fields.TextField(null=True, max_length=20)
    right_choice = fields.TextField(null=True, max_length=20)

    class Meta:
        """ Meta class for ActionText model """
        table = "actiontext"


class ActionIn(BaseModel):
    """ ActionIn pydantic model """
    tag: str
    previous: int = None
    next: int = None
    type: str
    position: PositionPost
    name: str
    description: str
    hint: str = None
    artifactID: int = None
    language: str
    # activityID: int
    targets: list[int] = None


class ChoiceMember(BaseModel):
    """ ChoiceMember pydantic model """
    target: int
    name: str


class ChoiceOut(BaseModel):
    """ ChoiceOut pydantic model """
    left: ChoiceMember
    right: ChoiceMember


class ActionInPatch(BaseModel):
    """ ActionIn pydantic model """
    # tag is optional but if it is set it can't be None
    tag:  Optional[StrictStr]
    previous: Optional[int]
    next: Optional[int]
    # type is optional but if it is set it can't be None
    type: Optional[StrictStr]
    artifactID: Optional[int] = None
    # position is optional but if it is set it can't be None
    position: Optional[PositionPost]
    # description is optional but if it is set it can't be None
    description:  Optional[StrictStr]
    # name is optional but if it is set it can't be None
    name:  Optional[StrictStr]
    hint: Optional[StrictStr] = None
    choice: Optional[ChoiceOut]
    targets: Optional[list[int]]

    # verify that choice is not None if type is choice
    @validator('choice')
    @classmethod
    def validate_choice(cls, value, values):
        """ Verify that choice is not None if type is choice """
        if value is None and values.get('type') == 'choice':
            raise ValueError("choice must be set if type is choice")
        return value

    @validator('name')
    @classmethod
    def validate_name(cls, value):
        """ Verify that choice is not None if type is choice """
        if value is None:
            raise ValueError("name value must be provided if key set")
        return value

    @validator('description')
    @classmethod
    def validate_description(cls, value):
        """ prevent description to be None if key set"""
        if value is None:
            raise ValueError("description value must be provided if key set")
        return value

    @validator('position')
    @classmethod
    def validate_position(cls, value):
        """ prevent position to be None if key set"""
        if value is None:
            raise ValueError("position value must be provided if key set")
        return value

    @validator('type')
    @classmethod
    def validate_type(cls, value):
        """ prevent type to be None if key set"""
        if value is None:
            raise ValueError("type value must be provided if key set")
        return value

    @validator('tag')
    @classmethod
    def validate_tag(cls, value):
        """ prevent tag to be None if key set"""
        if value is None:
            raise ValueError("tag value must be provided if key set")
        return value

    @validator('targets')
    @classmethod
    def validate_targets(cls, value):
        """ prevent targets to be None if key set"""
        if value is None:
            raise ValueError("targets value must be provided if key set")
        if len(value) == 0:
            raise ValueError("action must have at least one target")
        return value

    class Config:
        """ Config class for ActionInPatch pydantic model """
        extra = "forbid"


class ActionOut(BaseModel):
    """ ActionOut pydantic model """
    id: int
    tag: str
    hint: str | None
    previous: int | None
    next: int | None
    type: str
    position: PositionPost
    name: str
    description: str
    ressource: str | None
    artifactID: int | None
    choice: ChoiceOut | None
    targets: list[int]

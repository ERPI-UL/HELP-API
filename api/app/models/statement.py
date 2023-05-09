from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, StrictStr, validator
from tortoise import Model, fields


class Verb(Model):
    """ Model of an xAPI verb """
    id = fields.CharField(pk=True, max_length=200)


class Statement(Model):
    """ Model of a Performance Indico API statement,
        which is a substatement/inspiration of an xAPI statement
    """
    id = fields.IntField(pk=True)

    # author of the statement
    actor = fields.ForeignKeyField('models.User', related_name='statements', on_delete=fields.SET_NULL, null=True)

    # completed, attempted, passed, failed, answered, progressed, etc. list in json config file
    verb = fields.ForeignKeyField('models.Verb', related_name='statements', on_delete=fields.SET_NULL, null=True)

    # Jean start the activity 1
    object_activity = fields.ForeignKeyField('models.Activity', related_name='statements_objects', on_delete=fields.SET_NULL, null=True)
    # Jean start the action 42
    object_action = fields.ForeignKeyField('models.Action', related_name='statements', on_delete=fields.SET_NULL, null=True)
    # Jean pressed power_on
    object_target = fields.ForeignKeyField('models.Target', related_name='statements', on_delete=fields.SET_NULL, null=True)
    # Alex give a feedback to Jean
    object_agent = fields.ForeignKeyField('models.User', related_name='statements_as_agent', on_delete=fields.SET_NULL, null=True)

    # Jean succesfully completed the action 42
    result_success = fields.BooleanField(null=True)
    # skipped or completed
    result_completion = fields.BooleanField(null=True)
    # time spent on the object or action on the object
    result_duration = fields.IntField(null=True)

    # feedback to this statement
    result_response = fields.CharField(max_length=200, null=True)
    result_extensions = fields.JSONField()

    result_score_scaled = fields.FloatField(null=True)
    result_score_raw = fields.FloatField(null=True)
    result_score_min = fields.FloatField(null=True)
    result_score_max = fields.FloatField(null=True)

    context_platform = fields.ForeignKeyField('models.Platform', related_name='statements', on_delete=fields.SET_NULL, null=True)
    context_language = fields.ForeignKeyField('models.Language', related_name='statements', on_delete=fields.SET_NULL, null=True)
    context_activity = fields.ForeignKeyField('models.Activity', related_name='statements_context', on_delete=fields.SET_NULL, null=True)

    timestamp = fields.DatetimeField(null=True)
    stored = fields.DatetimeField(auto_now_add=True)

    class Meta:
        """ Meta class """
        ordering = ['-id']


class PlatformOut(BaseModel):
    """ Model of a platform """
    name: str


class ScoreInCreate(BaseModel):
    """ Model of an xAPI score """
    scaled: float = None
    raw: float = None
    min: float = None
    max: float = None


class ResultInCreate(BaseModel):
    """ Model of an xAPI result """
    success: bool = None
    completion: bool = None
    response: str = None
    duration: int = None
    score: ScoreInCreate = None
    extensions: dict = None


class AgentInCreate(BaseModel):
    """ Model of an xAPI agent """
    id: int
    objectType: Literal['agent']


class ActivityInCreate(BaseModel):
    """ Model of an xAPI activity """
    objectType: Literal['activity']
    id: int


class TargetInCreate(BaseModel):
    """ Model of an xAPI target """
    objectType: Literal['target']
    id: int


class ActionInCreate(BaseModel):
    objectType: Literal['action']
    id: int


class ContextInCreate(BaseModel):
    """ Model of an xAPI context """
    platform: Optional[StrictStr] = "Generic"
    language: Optional[StrictStr]
    activity: Optional[int]

    @validator('language')
    @classmethod
    def language_must_not_be_empty(cls, value):
        """ Validator for language """
        if value == "" or value is None:
            raise ValueError("Language value must not be empty or null")
        if len(value) != 2:
            raise ValueError("Language value must be 2 characters long in ISO 639-1 format")
        return value

    @validator('platform')
    @classmethod
    def platform_must_not_be_empty(cls, value):
        """ Validator for platform """
        if value == "" or value is None:
            raise ValueError("Platform value must not be empty or null")
        return value

    @validator('activity')
    @classmethod
    def activity_must_not_be_null(cls, value):
        """ Validator for activity """
        if value is None or value == 0:
            raise ValueError("Activity value must not be null")
        return value


class StatementInCreate(BaseModel):
    """ Model of an xAPI statement """
    # id: UUID4
    actor: int = None  # id of the user in the LMS
    verb: str  # id of the verb
    object: Union[
        ActivityInCreate,
        AgentInCreate,
        TargetInCreate,
        ActionInCreate
    ] = Field(..., discriminator='objectType')
    context: ContextInCreate = None
    result: ResultInCreate = None
    extensions: dict = None
    timestamp: datetime | None = None


class ObjectOut(BaseModel):
    """ Model of an xAPI object """
    objectType: Literal['activity', 'agent', 'target', 'action']
    id: int


class ContextOut(BaseModel):
    """ Model of an xAPI context """
    platform: Optional[StrictStr]
    language: Optional[StrictStr]
    activity: Optional[int]


class StatementOut(BaseModel):
    """ Model of an xAPI statement """
    id: int
    actor: int = None  # id of the user in the LMS
    verb: str  # id of the verb
    object: ObjectOut
    context: ContextOut = None
    result: ResultInCreate = None
    extensions: dict = None
    timestamp: datetime | None = None
    stored: datetime | None = None

    class Config:
        """ Config class for StatementOut model """
        orm_mode = True

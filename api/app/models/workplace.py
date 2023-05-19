from typing import Optional

from pydantic import BaseModel, validator
from tortoise import Model, fields

from app.models.artifact import Anchor
from app.types.position import Position


class WorkPlace(Model):
    """ WorkPlace model"""
    id = fields.IntField(pk=True)

    # anchor position
    x = fields.FloatField(default=None, null=True)
    y = fields.FloatField(default=None, null=True)
    z = fields.FloatField(default=None, null=True)
    # anchor orientation
    u = fields.FloatField(default=None, null=True)
    v = fields.FloatField(default=None, null=True)
    w = fields.FloatField(default=None, null=True)

    author = fields.ForeignKeyField(
        'models.User', related_name='workplaces', on_delete=fields.SET_NULL, null=True)

    class Meta:
        """ Meta class for WorkPlace model"""
        table = "workplaces"


class WorkPlaceText(Model):
    """ WorkPlaceText model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='workplaceTexts')
    workplace = fields.ForeignKeyField(
        'models.WorkPlace', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for WorkPlaceText model"""
        table = "workplacetext"


class ArtifactInstance(Model):
    """ ArtifactInstance model"""
    id = fields.IntField(pk=True)
    workplace = fields.ForeignKeyField('models.WorkPlace', related_name='instances', on_delete=fields.CASCADE)
    # position
    x = fields.FloatField()
    y = fields.FloatField()
    z = fields.FloatField()
    # angle
    u = fields.FloatField()
    v = fields.FloatField()
    w = fields.FloatField()

    artifact = fields.ForeignKeyField('models.Artifact', related_name='instances', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for ArtifactInstance model"""


class ArtifactInstanceIn(BaseModel):
    """ ArtifactInstanceIn pydantic model"""
    artifactID: int  # artifact id
    position: Position
    rotation: Position


class ArtifactInstanceOut(BaseModel):
    """ ArtifactInstanceOut pydantic model"""
    id: int
    artifactID: int
    position: Position
    rotation: Position


class ArtifactInstanceInPatch(BaseModel):
    """ ArtifactInstanceInPatch pydantic model"""
    artifactID: Optional[int]
    position: Optional[Position]
    rotation: Optional[Position]

    @validator('artifactID')
    @classmethod
    def artifact_not_none(cls, v):
        """ validator for artifactID"""
        if v is None:
            raise ValueError('artifactID value cannot be None')
        return v

    @validator('position')
    @classmethod
    def position_not_none(cls, v):
        """ validator for position"""
        if v is None:
            raise ValueError('position value cannot be None')
        return v

    @validator('rotation')
    @classmethod
    def rotation_not_none(cls, v):
        """ validator for rotation"""
        if v is None:
            raise ValueError('rotation value cannot be None')
        return v


class WorkplaceInPatch(BaseModel):
    """ WorkplaceInPatch pydantic model"""
    name: Optional[str]
    description: Optional[str]
    anchor: Optional[Anchor]

    @validator('name')
    @classmethod
    def name_not_none(cls, value):
        """ validator for name"""
        if value is None or value == '':
            raise ValueError('name value cannot be None')
        return value

    @validator('description')
    @classmethod
    def description_not_none(cls, value):
        """ validator for description"""
        if value is None or value == '':
            raise ValueError('description value cannot be None')
        return value


class WorkplaceIn(BaseModel):
    """ WorkplaceIn pydantic model"""
    name: str
    description: str
    language: str
    anchor: Anchor = None
    artifacts: list[ArtifactInstanceIn]


class WorkplaceOut(BaseModel):
    """ WorkplaceOut pydantic model"""
    id: int
    name: str
    description: str
    language: str
    anchor: Anchor = None
    artifacts: list[ArtifactInstanceOut]


class WorkplaceOutShort(BaseModel):
    """ WorkplaceOutShort pydantic model"""
    id: int
    name: str
    description: str
    languages: list[str]

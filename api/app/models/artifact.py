from pydantic import validator
from typing import Optional

from pydantic import BaseModel
from tortoise import Model, fields

from app.models.workplace import Position


class Artifact(Model):
    """ Artifact model , an object that is instantiated in the workplace"""
    id = fields.IntField(pk=True)
    author = fields.ForeignKeyField('models.User', related_name='artifacts', on_delete=fields.CASCADE, null=True)
    # anchor
    x = fields.FloatField(default=0)
    y = fields.FloatField(default=0)
    z = fields.FloatField(default=0)
    # angle
    u = fields.FloatField(default=0)
    v = fields.FloatField(default=0)
    w = fields.FloatField(default=0)


class ArtifactText(Model):
    """ ArtifactText model """
    id = fields.IntField(pk=True)
    name = fields.TextField(max_length=50)
    description = fields.TextField()
    artifact = fields.ForeignKeyField('models.Artifact', related_name='texts', on_delete=fields.CASCADE)
    language = fields.ForeignKeyField('models.Language', related_name='artifactTexts')


class Anchor(BaseModel):
    """ Anchor pydantic model """
    position: Position
    rotation: Position


class ArtifactInPatch(BaseModel):
    """ ArtifactInPatch pydantic model """
    name: Optional[str]
    description: Optional[str]
    anchor: Optional[Anchor]

    @validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        """ Validator for name """
        if v == "" or v is None:
            raise ValueError("Name value must not be empty or null")
        return v

    @validator('description')
    @classmethod
    def description_must_not_be_empty(cls, v):
        """ Validator for description """
        if v == "" or v is None:
            raise ValueError("Description value must not be empty or null")
        return v

    @validator('anchor')
    @classmethod
    def anchor_must_not_be_none(cls, v):
        """ Validator for anchor """
        if v is None:
            raise ValueError("Anchor value must not be null")
        return v


class ArtifactIn(BaseModel):
    """ ArtifactIn pydantic model """
    name: str
    description: str
    language: str
    anchor: Anchor

    @validator('language')
    @classmethod
    def language_must_be_2_chars(cls, v):
        """ Validator for language """
        if len(v) != 2:
            raise ValueError("Language value must be 2 characters long")
        return v


class ArtifactOut(BaseModel):
    """ ArtifactOut pydantic model """
    id: int
    name: str
    description: str
    language: str
    anchor: Anchor
    targets: list[int] = []


class ArtifactOutShort(BaseModel):
    """ ArtifactOut pydantic model """
    id: int
    name: str
    description: str
    languages: list[str]

    class Config:
        """ Config class for ArtifactOutShort model """
        orm_mode = True

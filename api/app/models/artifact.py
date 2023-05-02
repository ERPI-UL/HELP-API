from pydantic import validator
from typing import Optional

from pydantic import BaseModel
from tortoise import Model, fields


class Artifact(Model):
    """ Artifact model , an object that is instantiated in the workplace"""
    id = fields.IntField(pk=True)
    author = fields.ForeignKeyField('models.User', related_name='artifacts', on_delete=fields.CASCADE, null=True)


class ArtifactText(Model):
    """ ArtifactText model """
    id = fields.IntField(pk=True)
    name = fields.TextField(max_length=50)
    description = fields.TextField()
    artifact = fields.ForeignKeyField('models.Artifact', related_name='texts', on_delete=fields.CASCADE)
    language = fields.ForeignKeyField('models.Language', related_name='artifactTexts')


class ArtifactInPatch(BaseModel):
    """ ArtifactInPatch pydantic model """
    name: Optional[str]
    description: Optional[str]

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


class ArtifactIn(BaseModel):
    """ ArtifactIn pydantic model """
    name: str
    description: str
    language: str


class ArtifactOut(BaseModel):
    """ ArtifactOut pydantic model """
    id: int
    name: str
    description: str
    language: str
    targets: list[int] = []
    components: list[int] = []


class ArtifactOutShort(BaseModel):
    """ ArtifactOut pydantic model """
    id: int
    name: str
    description: str
    language: list[str]

    class Config:
        """ Config class for ArtifactOutShort model """
        orm_mode = True

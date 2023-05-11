from typing import Optional
from pydantic import BaseModel, StrictStr, validator
from tortoise import Model, fields


class Activity(Model):
    """ Activity model, an object that represents a lesson"""
    id = fields.IntField(pk=True)
    artifacts = fields.ManyToManyField('models.Artifact', related_name='activities', through='activity_artifact')
    start = fields.ForeignKeyField('models.Action', related_name='start_set', null=True, on_delete=fields.SET_NULL)


class ActivityText(Model):
    """ ActivityText model """
    id = fields.IntField(pk=True)
    name = fields.TextField(max_length=50)
    description = fields.TextField()
    language = fields.ForeignKeyField('models.Language', related_name='activityTexts')
    activity = fields.ForeignKeyField('models.Activity', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for ActivityText model """
        table = "activitytext"


class ActivityOut(BaseModel):
    """ ActivityOut pydantic model """
    id: int
    name: str
    description: str
    language: str
    start: int = None
    artifacts: list[int]

    class Config:
        """ Config class for ActivityOut model """
        orm_mode = True


class ActivityOutTrad(BaseModel):
    """ ActivityOut pydantic model """
    id: int
    name: str
    description: str
    language: list[str]
    start: int = None
    artifacts: list[int] | list

    class Config:
        """ Config class for ActivityOut model """
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Introduction à l'utilisation de la machine à café",
                "description": "Cette activité permet de découvrir les fonctionnalités de la machine à café.",
                "language": ["fr", "en"],
                "start": 1,
                "artifacts": [42]
            }
        }


class ActivityIn(BaseModel):
    """ ActivityIn pydantic model """
    name: str
    description: str
    language: str
    start: int | None
    artifacts: list[int]


class ActivityInPatch(BaseModel):
    """ ActivityInPatch pydantic model """
    name: Optional[StrictStr]
    description: Optional[StrictStr]
    start: Optional[int]
    artifacts: Optional[list[int]]

    @validator('name')
    @classmethod
    def check_name(cls, value):
        """ Check if name is valid """
        if value is not None:
            if len(value) > 50:
                raise ValueError('Name is too long')
        else:
            raise ValueError('Name value cannot be null')
        return value

    @validator('description')
    @classmethod
    def check_description(cls, value):
        """ Check if description is valid """
        if value is not None:
            if len(value) > 500:
                raise ValueError('Description is too long')
        else:
            raise ValueError('Description value cannot be null')
        return value

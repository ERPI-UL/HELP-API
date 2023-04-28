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

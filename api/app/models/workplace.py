from pydantic import BaseModel
from tortoise import Model, fields


class WorkPlace(Model):
    """ WorkPlace model"""
    id = fields.IntField(pk=True)
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
    x = fields.IntField()
    y = fields.IntField()
    z = fields.IntField()
    # angle
    u = fields.IntField()
    v = fields.IntField()
    w = fields.IntField()

    artifact = fields.ForeignKeyField('models.Artifact', related_name='instances', on_delete=fields.CASCADE)


class Position(BaseModel):
    """ Position pydantic model"""
    x: float
    y: float
    z: float


class ArtifactInstanceIn(BaseModel):
    """ ArtifactInstanceIn pydantic model"""
    id: int  # artifact id
    position: Position
    rotation: Position


class WorkplaceIn(BaseModel):
    """ WorkplaceIn pydantic model"""
    name: str
    description: str
    language: str
    artifacts: list[ArtifactInstanceIn]


class WorkplaceOut(BaseModel):
    """ WorkplaceOut pydantic model"""
    id: int
    name: str
    description: str
    language: str
    artifacts: list[ArtifactInstanceIn]


class WorkplaceOutShort(BaseModel):
    """ WorkplaceOutShort pydantic model"""
    id: int
    name: str
    description: str
    language: list[str]

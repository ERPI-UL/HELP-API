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


class ActivityOut(Model):
    """ ActivityOut pydantic model """
    id: int
    name: str
    description: str
    language: str
    start: int
    artifacts: list[int]

    class Config:
        """ Config class for ActivityOut model """
        orm_mode = True

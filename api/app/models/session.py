from datetime import datetime

from pydantic import BaseModel
from tortoise import Model, fields


class Session(Model):
    """
    Session model ,
    represent a session of an activity played by a user
    """
    id = fields.IntField(pk=True)
    # user can be null only if the user is deleted
    user = fields.ForeignKeyField('models.User', related_name='sessions', on_delete=fields.SET_NULL, null=True)
    activity = fields.ForeignKeyField('models.Activity', related_name='sessions', on_delete=fields.CASCADE)
    start = fields.DatetimeField()
    end = fields.DatetimeField(null=True)
    # calculated when end is set or when the session is retrieved
    duration = fields.IntField(null=True)
    # true when missing end on a session or action
    abandoned = fields.BooleanField(default=False)

    # stat for this session have already been computed
    computed = fields.BooleanField(default=False)

    # teacher fields
    mark = fields.FloatField(null=True)
    # x/20 or x/100 etc...
    denominator = fields.FloatField(null=True)
    comments = fields.TextField(null=True)


class ActionStats(Model):
    """
    ActionStats model ,
    represent an action played by a user in a session
    """
    id = fields.IntField(pk=True)
    session = fields.ForeignKeyField('models.Session', related_name='actionStats', on_delete=fields.CASCADE)
    action = fields.ForeignKeyField('models.Action', related_name='stats', on_delete=fields.CASCADE)
    start = fields.DatetimeField()
    end = fields.DatetimeField(null=True)
    duration = fields.IntField(null=True)
    completed = fields.BooleanField(default=False)
    # number of interactions with a component in a action
    interactions = fields.IntField(default=0)
    skipped = fields.BooleanField(default=False)
    # number of help request in a action
    help = fields.IntField(default=0)
    # stat for this action have already been computed
    computed = fields.BooleanField(default=False)


class SessionShort(BaseModel):
    """
    SessionShort pydantic model
    """
    id: int  # session id
    activity_id: int = None  # activity id
    start: datetime
    end: datetime = None
    duration: int = None
    abandoned: bool

    class Config:
        """ Config class """
        orm_mode = True

# ActionStats.get(action=action, session__user=user).order_by('start').first()

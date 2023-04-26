from datetime import datetime, timedelta

from tortoise import fields
from tortoise.models import Model


class Reset(Model):
    """ Reset model"""
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='reset')
    token = fields.CharField(128)
    expiration = fields.DatetimeField(
        default=datetime.now() + timedelta(days=1))

    class Meta:
        """ Meta class for Reset model"""
        table = "reset"

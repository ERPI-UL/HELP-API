from tortoise import fields
from tortoise.models import Model


class IncidentLogs(Model):
    """ IncidentLogs model"""
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='logs')
    date = fields.DatetimeField(auto_now_add=True)
    action = fields.TextField()

    class Meta:
        """ Meta class for IncidentLogs model"""
        table = "logs"

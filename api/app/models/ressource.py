from tortoise import fields
from tortoise.models import Model


class Ressource(Model):
    """ Ressource model , represent a file link to an object"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    path = fields.TextField()
    type = fields.TextField()

    class Meta:
        """ Meta class for Ressource model"""
        table = "ressources"

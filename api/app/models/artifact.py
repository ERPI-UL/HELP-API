from tortoise import Model, fields


class Artifact(Model):
    """ Artifact model , an object that is instantiated in the workplace"""
    id = fields.IntField(pk=True)

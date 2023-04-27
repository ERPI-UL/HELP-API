from tortoise import Model, fields


class Activity(Model):
    """ Activity model, an object that represents a lesson"""
    id = fields.IntField(pk=True)

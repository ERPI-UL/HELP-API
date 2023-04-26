from tortoise import Model, fields


class Activity(Model):
    id = fields.IntField(pk=True)

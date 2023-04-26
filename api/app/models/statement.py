from tortoise import Model, fields


class Verb(Model):
    """ Model of an xAPI verb """
    id = fields.CharField(pk=True, max_length=200)
    canonical = fields.JSONField()


class Agent(Model):
    """ Model of an xAPI agent """
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=200)
    mbox = fields.CharField(max_length=200)


class Statement(Model):
    """ Model of an xAPI statement """
    id = fields.UUIDField(pk=True)
    verb = fields.CharField(max_length=200)
    object = fields.CharField(max_length=200)
    actor = fields.CharField(max_length=200)
    context = fields.CharField(max_length=200)

from tortoise import Model, fields


class Component(Model):
    """ Component model , represent a file link to an object"""
    id = fields.IntField(pk=True)
    name = fields.TextField()

    class Meta:
        """ Meta class for Ressource model"""
        table = "components"


class Property(Model):
    """ Property model , represent a file link to an object"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    value = fields.TextField()
    properties = fields.ForeignKeyField('models.Component', related_name='properties', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for Ressource model"""
        table = "properties"

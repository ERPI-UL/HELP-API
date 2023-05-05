from tortoise import fields
from tortoise.models import Model


class Platform(Model):
    """
    Platform model , represent a device or a software that use the application
    """
    name = fields.CharField(pk=True, max_length=50)

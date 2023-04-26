from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Language(Model):
    """ Language model"""
    id = fields.IntField(pk=True)
    unicode = fields.CharField(128)  # \uD83C\uDDEB\uD83C\uDDF7 -> 🇫🇷
    name = fields.CharField(42)  # Français English Español
    code = fields.CharField(2)  # ISO 639-1 en fr en de it etc..

    class Meta:
        """ Meta class for Language model"""
        table = "languages"


LanguageOut = pydantic_model_creator(
    Language, name='LanguageFront', exclude_readonly=True)
LanguageOutWithId = pydantic_model_creator(
    Language, name='LanguageFrontWithId')

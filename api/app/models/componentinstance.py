from typing import Optional

from pydantic import BaseModel, StrictStr, validator
from tortoise import Model, fields


class ComponentInstance(Model):
    """ ComponentInstance model , represent a file link to an object"""
    id = fields.IntField(pk=True)
    tag = fields.CharField(max_length=50)
    type = fields.CharField(max_length=50)
    target = fields.ForeignKeyField('models.Target', related_name='componentInstances', on_delete=fields.CASCADE)
    script = fields.TextField()
    blocks = fields.TextField()


class PropertyInstance(Model):
    """ PropertyInstance model , represent a file link to an object"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    value = fields.CharField(max_length=500)
    componentInstance = fields.ForeignKeyField('models.ComponentInstance', related_name='properties', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for Ressource model"""
        table = "propertyInstances"


class PropertyInstanceIn(BaseModel):
    """ PropertyInstanceIn pydantic model"""
    name: str
    value: str
    # componentInstance: int


class ComponentInstanceIn(BaseModel):
    """ ComponentInstanceIn pydantic model"""
    tag: str
    type: str
    target: int
    script: str
    blocks: str
    properties: list[PropertyInstanceIn] = []


class ComponentInstanceOut(BaseModel):
    """ ComponentInstanceOut pydantic model"""
    id: int
    tag: str
    type: str
    target: int
    script: str
    blocks: str
    properties: list[PropertyInstanceIn] = []

    class Config:
        """ Config class for ComponentInstanceOut model """
        orm_mode = True


class PropertyInstanceInPatch(BaseModel):
    """ PropertyInstanceInPatch pydantic model"""
    name: Optional[str]
    value: Optional[str]

    @validator('name')
    @classmethod
    def name_value_validator(cls, value):
        """ name_value_validator validator for PropertyInstanceInPatch model"""
        if value is None or value == "":
            raise ValueError("name value cannot be empty")
        return value

    @validator('value')
    @classmethod
    def value_value_validator(cls, value):
        """ value_value_validator validator for PropertyInstanceInPatch model"""
        if value is None:
            raise ValueError("value value cannot be null")
        return value

    class Config:
        """ Config class for PropertyInstanceInPatch model """
        orm_mode = True


class ComponentInstanceInPatch(BaseModel):
    """ ComponentInstanceInPatch pydantic model"""
    tag: Optional[StrictStr]
    type: Optional[StrictStr]
    target: Optional[int]
    script: Optional[StrictStr]
    blocks: Optional[StrictStr]
    properties: list[PropertyInstanceInPatch] = []

    @validator('tag')
    @classmethod
    def tag_value_validator(cls, value):
        """ tag_value_validator validator for ComponentInstanceInPatch model"""
        if value is None or value == "":
            raise ValueError("tag value cannot be empty")
        return value

    @validator('target')
    @classmethod
    def target_value_validator(cls, value):
        """ target_value_validator validator for ComponentInstanceInPatch model"""
        if value is None:
            raise ValueError("target value cannot be null")
        return value

    @validator('script')
    @classmethod
    def script_value_validator(cls, value):
        """ script_value_validator validator for ComponentInstanceInPatch model"""
        if value is None:
            raise ValueError("script cannot be null")
        return value

    @validator('blocks')
    @classmethod
    def blocks_value_validator(cls, value):
        """ blocks_value_validator validator for ComponentInstanceInPatch model"""
        if value is None:
            raise ValueError("blocks cannot be null")
        return value

    @validator('type')
    @classmethod
    def type_value_validator(cls, value):
        """ type_value_validator validator for ComponentInstanceInPatch model"""
        if value is None:
            raise ValueError("type cannot be null")
        return value

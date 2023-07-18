from typing import Any
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
    properties = fields.JSONField(default=[])


class PropertyInstanceIn(BaseModel):
    """ PropertyInstanceIn pydantic model"""
    name: str
    value: Any


class ComponentInstanceIn(BaseModel):
    """ ComponentInstanceIn pydantic model"""
    tag: str
    type: str
    target: int
    script: str
    blocks: str
    properties: list[PropertyInstanceIn]


class ComponentInstanceOut(BaseModel):
    """ ComponentInstanceOut pydantic model"""
    id: int
    tag: str
    type: str
    target: int
    script: str
    blocks: str
    properties: list[PropertyInstanceIn]

    class Config:
        """ Config class for ComponentInstanceOut model """
        orm_mode = True


class ComponentInstanceInPatch(BaseModel):
    """ ComponentInstanceInPatch pydantic model"""
    tag: Optional[StrictStr]
    type: Optional[StrictStr]
    target: Optional[int]
    script: Optional[StrictStr]
    blocks: Optional[StrictStr]
    properties: Optional[list[PropertyInstanceIn]]

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of permissions schema
"""
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field
import peewee as pw
from pydantic.utils import GetterDict

from schemas import AllOptional


class CampaignNodePermGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == 'node':
            return self._obj.node.id
        if key == 'user':
            return self._obj.user.id
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class CampaignNodePermission(BaseModel):
    """CampaignNodePermission object"""
    node: int = Field(..., description='Node related with this permission', example=0)
    user: int = Field(..., description='User related with this permission', example=0)
    can_view: Optional[bool] = Field(False, description='If the user can view the node data', example=False)
    can_submit: Optional[bool] = Field(False, description='If the user can submit data to the node', example=False)
    can_see_data: Optional[bool] = Field(False, description='If the user can see submitted data', example=False)
    can_edit: Optional[bool] = Field(False, description='If the user can edit the data', example=False)

    class Config:
        orm_mode = True
        getter_dict = CampaignNodePermGetter


class CampaignNodePermissionOut(CampaignNodePermission):
    created_at: Optional[datetime] = Field(..., description='When the campaign was created', example=datetime.utcnow())
    updated_at: Optional[datetime] = Field(..., description='When the campaign was edited', example=datetime.utcnow())


class CampaignNodePermissionUpdate(CampaignNodePermission, metaclass=AllOptional):
    pass

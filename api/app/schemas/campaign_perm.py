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


class CampaignPermGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == 'campaign':
            return self._obj.campaign.id
        if key == 'user':
            return self._obj.user.id
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class CampaignPermission(BaseModel):
    """CampaignPermission object"""
    campaign: int = Field(..., description='Campaign related with this permission', example=0)
    user: int = Field(..., description='User related with this permission', example=0)
    can_view: bool = Field(True, description='If the user can view the campaign', example=True)
    can_edit: bool = Field(False, description='If the user can edit the campaign', example=False)
    can_view_inherited: bool = Field(False, description='If the permission on if the user can view the campaign'
                                                        ' is inherited.', example=False)
    can_edit_inherited: bool = Field(False, description='If the permission on if the user can edit the campaign'
                                                        ' is inherited.', example=False)
    created_at: Optional[datetime] = Field(..., description='When the campaign was created', example=datetime.utcnow())
    updated_at: Optional[datetime] = Field(..., description='When the campaign was edited', example=datetime.utcnow())

    class Config:
        orm_mode = True
        getter_dict = CampaignPermGetter


class CampaignPermissionIn(BaseModel):
    can_view: Optional[bool] = Field(None, description='If the user can view the campaign', example=True, null=True)
    can_edit: Optional[bool] = Field(None, description='If the user can edit the campaign', example=False, null=True)

    class Config:
        orm_mode = True
        getter_dict = CampaignPermGetter

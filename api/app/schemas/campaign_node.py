#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of a campaign schema
"""

from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field, Json
from pydantic.utils import GetterDict
import peewee as pw

from schemas import AllOptional


class CampaignNodeGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == 'parent':
            return self._obj.parent.id
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class CampaignNode(BaseModel):
    """CampaignNode object"""
    parent: int = Field(..., description='The parent node', example=0)
    data: Json = Field(..., description='The node data', example={})

    can_submit: Optional[bool] = Field(False, description='If the node can have data submitted.', example=False)
    can_submit_more_than_once: Optional[bool] = Field(False, description='If the node can have data submitted.', example=False)
    must_be_submitted: Optional[bool] = Field(False, description='If the node must have data submitted if applicable '
                                                     'and if all children node have been validated.', example=False)

    everyone_can_see: Optional[bool] = Field(False, description='If the node can been seen by everyone by default.', example=False)
    everyone_can_submit: Optional[bool] = Field(False, description='If everyone can submit data by default', example=False)
    is_hidden: Optional[bool] = Field(False, description='If the node is hidden from people who can\'t see data. '
                                             'Override everyone_can_see.', example=False)

    class Config:
        orm_mode = True
        getter_dict = CampaignNodeGetter


class CampaignNodeOut(CampaignNode):
    id: Optional[int] = Field(None, description='Campaign Node identifier')
    created_at: Optional[datetime] = Field(..., description='When the campaign node was created', example=datetime.utcnow())


class CampaignNodeUpdate(CampaignNode, metaclass=AllOptional):
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of Campaign schema
"""

from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field
from pydantic.utils import GetterDict
import peewee as pw

from schemas import AllOptional


class CampaignGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == 'owner':
            return self._obj.owner.id
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class Campaign(BaseModel):
    """Campaign schema"""
    name: str = Field(..., description='News name', example='Answering to the Ultimate Question of Life,'
                                                            'The Universe, and Everything')
    description: str = Field("", description='Campaign Description',
                             example='The Answer to the Ultimate Question of Life'
                                     ',The Universe, and Everything is the most important question.'
                                     'With this campaign you will help us to answer it.')
    root: int = Field(None, description='Which node is the root', example=0)
    is_public: Optional[bool] = Field(False, description='If the campaign is public', example=False)

    class Config:
        orm_mode = True
        getter_dict = CampaignGetter


class CampaignOut(Campaign):
    id: Optional[int] = Field(None, description='News identifier')
    owner: int = Field(..., description='Who owned the campaign', example=0)
    created_at: Optional[datetime] = Field(..., description='When the campaign was created', example=datetime.utcnow())
    updated_at: Optional[datetime] = Field(..., description='When the campaign was edited', example=datetime.utcnow())


class CampaignUpdate(Campaign, metaclass=AllOptional):
    pass

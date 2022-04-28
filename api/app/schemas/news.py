#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of news of a campaign schema
"""
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field
import peewee as pw
from pydantic.utils import GetterDict

from schemas import AllOptional


class NewsGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == 'campaign':
            return self._obj.campaign.id
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class News(BaseModel):
    """News object"""
    name: str = Field(..., description='News name', example='Why the Answer to the Ultimate Question of Life,'
                                                            + 'The Universe, and Everything is 42 ?')
    campaign: int = Field(..., description='Campaign which the news is about', example=0)

    class Config:
        orm_mode = True
        getter_dict = NewsGetter


class NewsOut(News):
    id: Optional[int] = Field(None, description='News identifier')
    author: int = Field(..., description='Author who wrote the article', example=0)
    created_at: Optional[datetime] = Field(..., description='When the news was created', example=datetime.utcnow())
    updated_at: Optional[datetime] = Field(..., description='When the news was edited', example=datetime.utcnow())


class NewsUpdate(News, metaclass=AllOptional):
    pass


class NewContent(BaseModel):
    """News content schema
    The content is moved to another schema to avoid transferring too much data when asking the news
    """
    content: Optional[str] = Field(None, description='Contant of the news',
                                   example='Lorem ipsum dolor sit amet, consectetur adipiscing elit. In euismod feli'
                                           + 'eget nulla porta, sed condimentum magna hendrerit.')
